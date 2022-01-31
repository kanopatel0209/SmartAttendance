from django.views import View
from django.shortcuts import render
from django.http import JsonResponse
from institute.admin import institute_admin_site
from institute.models import UniversityBranch
from institute.shared.exportfile import export_data

# Create your views here.
class DashboardView(View):
  
  def get(self, request, **kwargs):
    branch_list = []
    for item in UniversityBranch.objects.all().values():
      name = item['branch_name']
      if name not in branch_list:
        branch_list.append(name)

    context = institute_admin_site.each_context(request)
    context.update({
      "branch": branch_list,
      "semester": sorted(set(x['semester'] for x in UniversityBranch.objects.values('semester'))),
      "title": "Dashboard"
    })
    return render(
      request,
      "institute/dashboard.html",
      context=context,
    )

  def post(self, request, **kwargs):
    events = export_data(branch_name=request.POST["branch"])
    return JsonResponse({"Events": events})
