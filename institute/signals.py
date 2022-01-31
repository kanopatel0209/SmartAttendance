import os
from django.db.models.signals import (
  m2m_changed, post_init,
  pre_save, post_save,
  pre_delete, post_delete)
from django.dispatch.dispatcher import receiver
from django.contrib.auth.models import Group, User
from institute.models import (
  UniversityBranch,
  TeacherProfile,
  StudentProfile,
  AcademicLesson
)

from institute.shared.img2lable import encodeProfile, facesInImage, compareFaces


def set_is_elect_true(sender, instance, action, model, pk_set, **kwargs):
  if action=='post_add':
    for pk in pk_set:
      sub = model.objects.get(id=pk)
      if not sub.is_elect:
        sub.is_elect = True
        sub.save()
  if action=='pre_remove':
    for pk in pk_set:
      sub = model.objects.get(id=pk)
      if len(sub.universitybranch_set.all()) < 2:
        sub.is_elect = False
        sub.save()
m2m_changed.connect(set_is_elect_true, sender=UniversityBranch.subject.through)


def file_associated(sender, instance, context):
  new_file = getattr(instance, context['img_field'])
  default = sender._meta.get_field(new_file.field.name).get_default()
  try:
    old_file = getattr(sender.objects.get(**context['key']), context['img_field'])
  except:
    if new_file != default:
      return True
  else:
    if new_file:
      if old_file.name != new_file.name:
        if old_file.name and old_file.name != default:
          os.remove(old_file.path)
        return True
    elif old_file.name != default:
      os.remove(old_file.path)
      setattr(instance, context['img_field'], default)
      return False


@receiver(pre_save, sender=User)
def set_default_active_status(sender, instance, **kwargs):
  for separator in ['.', '-']:
    name = instance.username.split(separator)
    if len(name) > 1:
      instance.last_name = name[1].capitalize()
      instance.first_name = name[0].capitalize()
      break

  # instance.is_active = False


@receiver(pre_save, sender=StudentProfile)
def encode_profile_in_binary(sender, instance, **kwargs):
  context = {
    'img_field':'std_profile_img',
    'key': {'enrollment': instance.enrollment}
  }
  instance.profile_encode = b''
  try:
    if file_associated(sender, instance, context):
      instance.profile_encode = encodeProfile(file_path=instance.std_profile_img._get_file())
  except:
    pass
    # DEV: person not found in image


@receiver(post_save, sender=TeacherProfile)
@receiver(post_save, sender=StudentProfile)
def add_group(sender, instance, **kwargs):
  try:
    if instance.user.is_active:
      if not instance.user.groups.filter(name='Student'):
        instance.user.groups.add(Group.objects.get(name='Student'))
      elif not instance.user.groups.filter(name='Staff'):
        instance.user.groups.add(Group.objects.get(name='Staff'))
  except:
    pass
    # DEV: redirect request to group section


@receiver(pre_delete, sender=TeacherProfile)
@receiver(pre_delete, sender=StudentProfile)
def remove_profile_img(sender, instance, **kwargs):
  # instance.user.is_active = False

  if sender.__name__ == 'TeacherProfile':
    existing_file = instance.tch_profile_img
  elif sender.__name__ == 'StudentProfile':
    existing_file = instance.std_profile_img
  
  default = sender._meta.get_field(existing_file.field.name).get_default()
  if existing_file and existing_file.path != default:
    os.remove(existing_file.path)


@receiver(post_delete, sender=TeacherProfile)
@receiver(post_delete, sender=StudentProfile)
def delete_user_instance(sender, instance, **kwargs):
  instance.user.groups.clear()
  instance.user.delete()



@receiver(pre_save, sender=AcademicLesson)
def check_for_new_image(sender, instance, **kwargs):
  context = {
    'img_field':'class_img',
    'key': {'id': instance.id}
  }
  instance._check_has_new_file = file_associated(sender, instance, context)


@receiver(post_save, sender=AcademicLesson)
def faces_in_class_img(sender, instance, **kwargs):
  if instance._check_has_new_file:
    faces = facesInImage(file_path=instance.class_img._get_file())
    sub = instance.sub_id
    for branch in sub.universitybranch_set.all():
      for std in branch.studentprofile_set.all():
        if std.profile_encode and compareFaces(faces, std.profile_encode):
          instance.student.add(std)
  

@receiver(pre_delete, sender=AcademicLesson)
def delete_class_img(sender, instance, **kwargs):
  if instance.class_img:
    os.remove(instance.class_img.path)

