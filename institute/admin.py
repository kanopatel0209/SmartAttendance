from django.contrib import messages
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import User, Group
from django.templatetags.static import static
from institute.adminsite import institute_admin_site, CustomModelAdmin
from institute.shared.exportfile import export_class_summary, export_individual_summary
from institute.models import (
  UniversityBranch,
  UniversitySubject,
  StudentProfile,
  TeacherProfile,
  AcademicLesson
)

UserAdmin.list_display += ('is_active',)
GroupAdmin.filter_horizontal += ('permissions',)

# Register your models here.

class UniversityBranchsModelAdmin(CustomModelAdmin):
  list_display = ('branch_name', 'semester')
  search_fields = ('branch_name',)
  list_filter = ('branch_name', 'semester')
  filter_horizontal= ('subject',)
  # ordering = ("branch_name", "semester")


  actions = ['to_excel']
  @admin.action(description='Export to excel')
  def to_excel(self, request, queryset):
    if len(queryset) > 1:
      self.message_user(request, "select only one item for single excel file", messages.WARNING)
    else:
      return export_class_summary(branch_name=queryset[0].branch_name, semester=queryset[0].semester)

  
  class Media:
    # js = (static("institute/js/custom_admin.js"),)
    css = {'all':(static("institute/css/custom_admin.css"),)}



class UniversitySubjectModelAdmin(CustomModelAdmin):
  list_display = ('subject_code', 'subject_name', 'is_elect')
  search_fields = ('subject_code', 'subject_name')
  list_filter = ('universitybranch__branch_name', 'universitybranch__semester')
  readonly_fields = ('is_elect',)
  # list_editable = ('is_elect',)
  # exclude = ('is_elect',)
  # ordering = ("subject_code", "subject_name")


  class Media:
    # js = (static("institute/js/custom_admin.js"),)
    css = {'all':(static("institute/css/custom_admin.css"),)}



class StudentProfileModelAdmin(CustomModelAdmin):
  list_display = ('enrollment', 'user', 'branch_name', 'semester', 'std_profile_img')
  search_fields = ('enrollment',)
  list_filter = ('branch__branch_name', 'branch__semester')
  # ordering = ("branch", "enrollment")

  
  def branch_name(self, obj):
    return obj.branch.branch_name
  def semester(self, obj):
    return obj.branch.semester

  branch_name.admin_order_field  = 'branch'

  actions = ['to_excel']
  @admin.action(description='Export to excel')
  def to_excel(self, request, queryset):
    if len(queryset) > 1:
      self.message_user(request, "select only one item for single excel file", messages.WARNING)
    else:
      return export_individual_summary(enrollment=queryset[0].enrollment)
  
  
  class Media:
    # js = (static("institute/js/custom_admin.js"),)
    css = {'all':(static("institute/css/custom_admin.css"),)}



class TeacherProfileModelAdmin(CustomModelAdmin):
  list_display = ('user', 'tch_profile_img')
  search_fields = ('user__username',)
  filter_horizontal= ('tch_sub',)

  def get_form(self, request, obj=None, change=False, **kwargs):
    form = super().get_form(request, obj=None, change=False, **kwargs)
    form.base_fields['user'].error_messages.update({
      'invalid_choice': 'You are not staff member'
    })
    return form

  class Media:
    # js = (static("institute/js/custom_admin.js"),)
    css = {'all':(static("institute/css/custom_admin.css"),)}



class AcademicLessonModelAdmin(CustomModelAdmin):
  # fields = ('date', 'sub_id', ('class_type', 'slot'), 'class_img', 'student')
  list_display = ('date', 'sub_id', 'class_type', 'slot', 'class_img')
  list_filter = ('class_type', 'slot', 'date')
  # ordering = ('-date', 'slot')
  # filter_horizontal = ('student',)
  # exclude = ('student',)
  

  def get_readonly_fields(self, request, obj=None):
    self.readonly_fields = ('student',)
    """
    Hook for specifying custom readonly fields.
    """
    if [gp for gp in request.user.groups.all() if str(gp)=='HOD1']:
      self.readonly_fields = ()
      self.filter_horizontal = ('student',)
    return self.readonly_fields


  class Media:
    # js = (static("institute/js/custom_admin.js"),)
    css = {'all':(static("institute/css/custom_admin.css"),)}




admin.site.register(UniversityBranch, UniversityBranchsModelAdmin)
admin.site.register(UniversitySubject, UniversitySubjectModelAdmin)
admin.site.register(StudentProfile, StudentProfileModelAdmin)
admin.site.register(TeacherProfile, TeacherProfileModelAdmin)
admin.site.register(AcademicLesson, AcademicLessonModelAdmin)


institute_admin_site.register(User, UserAdmin)
institute_admin_site.register(Group, GroupAdmin)
institute_admin_site.register(UniversityBranch, UniversityBranchsModelAdmin)
institute_admin_site.register(UniversitySubject, UniversitySubjectModelAdmin)
institute_admin_site.register(StudentProfile, StudentProfileModelAdmin)
institute_admin_site.register(TeacherProfile, TeacherProfileModelAdmin)
institute_admin_site.register(AcademicLesson, AcademicLessonModelAdmin)
