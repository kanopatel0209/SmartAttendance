from django.contrib import admin
from django.urls import reverse
from institute.shared.filters import check_filter_field

class CustomModelAdmin(admin.ModelAdmin):

  def get_list_filter(self, request):
    return check_filter_field(self.model, self.list_filter)


class InstituteAdminSite(admin.AdminSite):

  site_header = "Smart Attendance"
  site_title = "Smart Attendance Admin Portal"
  index_title = "Welcome to Smart Attendance Portal"

  def get_app_list(self, request):
    app_list = super().get_app_list(request)
    app_list.append(
      {
        'name': 'Analysis',
        'app_label': 'analysis',
        'app_url': '#',
        'has_module_perms': False, #True,
        'models': [
          {
            'name': 'Dashboard',
            'object_name': 'dashboard',
            # 'perms':
            # {
            #   'add': False,
            #   'change': False,
            #   'delete': False,
            #   'view': False
            # },
            'admin_url': reverse('dashboard'),
            # 'admin_url': None,
            # 'add_url': None,
            'view_only': True
          },
        ]
      }
    )
    return app_list

institute_admin_site = InstituteAdminSite(name='event_admin')
