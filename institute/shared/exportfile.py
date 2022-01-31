import pandas as pd
from io import BytesIO
from django.http import HttpResponse
from institute.models import UniversityBranch, StudentProfile, AcademicLesson


def export_data(branch_name):
  context = []
  
  branch_list = UniversityBranch.objects.filter(branch_name=branch_name)
  
  for branch in branch_list:
    for subject in branch.subject.all():
      for lesson in subject.academiclesson_set.all():
        data = {
          'name': str(subject.subject_name),
          'date': lesson.date,
          'class_type': lesson.class_type,
          'slot': lesson.slot,
          'semester': branch.semester,
          'student': [student.user.get_full_name() or student.user.username for student in lesson.student.all()]
        }
      context.append(data)
  return context



class ExportFile():
  def __init__(self, filename, ext):
    self.sio = BytesIO()
    self.writer = pd.ExcelWriter(self.sio, engine='xlsxwriter')
    self.filename = filename
    self.ext = ext
    
  def __enter__(self):
    # if self.exe == 'xlsx':
    self.content_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    return self

  def __exit__(self, exc_type, exc_value, exc_traceback):
    if exc_traceback:
      exc_traceback()

  @property
  def response(self):
    self.writer.save()   
    self.sio.seek(0)
    workbook = self.sio.getvalue()
    response = HttpResponse(workbook, self.content_type)
    response['Content-Disposition'] = f'attachment; filename="{self.filename}.xlsx"'
    return response


    
def export_class_summary(branch_name, semester):
  branch = UniversityBranch.objects.get(branch_name=branch_name, semester=semester)
  df_assemble = {'enrollment': [], 'name': []}
  for std in branch.studentprofile_set.order_by('enrollment'):
    df_assemble['enrollment'].append(std.enrollment)
    df_assemble['name'].append(std.user.get_full_name())
  df = pd.DataFrame(df_assemble, columns=['enrollment', 'name']).set_index(['enrollment'])

  file_name = f"{branch_name} (sem {semester})"
  
  with ExportFile(filename=file_name, ext='xlsx') as excel:
    
    for subject in branch.subject.order_by('subject_code'):
      df1 = df.copy()
      for lesson in subject.academiclesson_set.order_by('date', 'sub_id', 'slot'):
        ser = pd.Series(data=lesson.class_type[:3]+'-'+lesson.slot, name=lesson.date, index=[student.enrollment for student in lesson.student.order_by('enrollment')])
        df1 = df1.join(ser)
      df1.index.astype('int64')

      sheets_name = subject.subject_code + ' - ' + ''.join([d[0] for d in subject.subject_name.split()])

      df1.to_excel(excel.writer, sheet_name=sheets_name, na_rep='---')
      worksheet = excel.writer.sheets[sheets_name]
      worksheet.set_column('A:A', 16)
      worksheet.set_column('B:B', 20)
      worksheet.set_column('C:Z', 12)
    
    return excel.response



def export_individual_summary(enrollment):
  student = StudentProfile.objects.get(enrollment=enrollment)
  df = pd.DataFrame(columns=[j+i[0] for i in AcademicLesson.class_type.field.choices for j in ['total_', 'attend_']])
    
  df1 = df.copy()
  for subject in student.branch.subject.all():
    for col in df.columns:
      kwargs = {'sub_id':subject, 'class_type':col.split('_', 1)[1]}
      if col.startswith('total_'):
        df1.at[subject, col] = AcademicLesson.objects.filter(**kwargs).count()
      else:
        df1.at[subject, col] = student.academiclesson_set.filter(**kwargs).count()  
  
  file_name = student.user.get_full_name()
  sheets_name = student.enrollment

  with ExportFile(filename=file_name, ext='xlsx') as excel:
    df1.to_excel(excel.writer, sheet_name=sheets_name)
    
    worksheet = excel.writer.sheets[sheets_name]
    worksheet.set_column('A:A', 60)
    worksheet.set_column('B:F', 14)
    
    return excel.response

