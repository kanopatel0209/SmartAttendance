from django.db import models
from django.contrib.auth.models import User

def path_to_upload_image(instance, filename):
  if instance.__class__.__name__ == "StudentProfile":
    return f"UserProfiles/{instance.__class__.__name__}s/{instance.branch.branch_name}/{instance.branch.semester}/{filename}"
  elif instance.__class__.__name__ == "TeacherProfile":
    return f"UserProfiles/{instance.__class__.__name__}s/{filename}"

# Create your models here.

class UniversityBranch(models.Model):
  branch_name = models.CharField(max_length=50)
  semester = models.CharField(
    max_length=1,
    choices=[
      ("1", 1),
      ("2", 2),
      ("3", 3),
      ("4", 4),
      ("5", 5),
      ("6", 6),
      ("7", 7),
      ("8", 8),
    ],
  )
  subject = models.ManyToManyField("UniversitySubject")

  def __str__(self):
    return f"{self.semester} | {self.branch_name}"

  class Meta:
    verbose_name = "University Branch"
    unique_together = [("branch_name", "semester")]
    ordering = ("branch_name", "semester")


class UniversitySubject(models.Model):
  subject_code = models.CharField(max_length=7)
  subject_name = models.CharField(max_length=50)
  is_elect = models.BooleanField(default=False)

  def __str__(self):
    return f"{self.subject_code} - {self.subject_name}"

  class Meta:
    verbose_name = "University Subject"
    unique_together = [("subject_code", "subject_name")]
    ordering = ("subject_code", "subject_name")


class StudentProfile(models.Model):
  enrollment = models.CharField(max_length=12)
  user = models.OneToOneField(
    User, on_delete=models.CASCADE, limit_choices_to={"is_staff": False, "is_active": True}
  )
  std_profile_img = models.ImageField(
    upload_to=path_to_upload_image,
    default="UserProfiles/default_profile.jpg",
    blank=True,
  )
  branch = models.ForeignKey("UniversityBranch", on_delete=models.PROTECT)
  profile_encode = models.BinaryField(blank=True)

  def user_name(self):
    return f"{self.user.first_name} {self.user.last_name}"

  def __str__(self):
    return f"{self.user.username} Profile"

  class Meta:
    verbose_name = "Student Profile"
    ordering = ("branch", "enrollment")


class TeacherProfile(models.Model):
  user = models.OneToOneField(
    User,
    on_delete=models.CASCADE,
    limit_choices_to={"is_staff": True, "is_active": True},
    help_text="Only staff member available for choice selection"
  )
  tch_profile_img = models.ImageField(
    upload_to=path_to_upload_image,
    default="UserProfiles/default_profile.jpg",
    blank=True,
  )
  tch_sub = models.ManyToManyField(
    "UniversitySubject", limit_choices_to={"is_elect": True}
  )

  def user_name(self):
    return f"{self.user.first_name} {self.user.last_name}"

  def __str__(self):
    return f"{self.user.username} Profile"

  class Meta:
    verbose_name = "Teacher Profile"


def path_to_upload_media(instance, filename):
  return f"ClassImages/{instance.sub_id.subject_code}/{instance.date}.{filename.rsplit('.', 1)[1]}"


class AcademicLesson(models.Model):

  date = models.DateField()
  sub_id = models.ForeignKey(
    "UniversitySubject",
    on_delete=models.CASCADE,
    limit_choices_to={"is_elect": True},
  )
  class_type = models.CharField(
    max_length=7, choices=[("lecture", "Lecture"), ("lab", "Lab")]
  )
  slot = models.CharField(
    max_length=1,
    choices=[
      ("1", "1"),
      ("2", "2"),
      ("3", "3"),
      ("4", "4"),
      ("5", "5"),
      ("6", "6"),
    ],
  )
  class_img = models.ImageField(upload_to=path_to_upload_media, default="ClassImages/default_image.jpg", blank=True)
  student = models.ManyToManyField("StudentProfile")

  def __str__(self):
    return f"{self.date} | {self.sub_id}"

  class Meta:
    verbose_name = "Academic Lesson"
    ordering = ('-date', 'slot')
