from django.contrib import admin
from .models import  (Student, StudentBulkUpload)
from apps.corecode.models import AcademicSession, AcademicTerm, StudentClass, Subject
from apps.staffs.models import Staff

# Register your models here.
admin.site.register(Student)
admin.site.register(AcademicSession)
admin.site.register(AcademicTerm)
admin.site.register(StudentClass)

admin.site.register(Subject)
# admin.site.register(StudentBulkUpload)

admin.site.register(Staff)