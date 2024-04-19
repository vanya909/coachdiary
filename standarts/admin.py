from django.contrib import admin
from .models import Level, Gender, Classes, Students, Grades, Standards, StandardsValues, StudentsStandards

# Register your models here.
admin.site.register(Level)
admin.site.register(Gender)
admin.site.register(Classes)
admin.site.register(Students)
admin.site.register(Grades)
admin.site.register(Standards)
admin.site.register(StandardsValues)
admin.site.register(StudentsStandards)
