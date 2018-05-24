from django.contrib import admin
from dataParser.models import StudentInfo
from django.contrib.auth.admin import UserAdmin
# Register your models here.
admin.site.register(StudentInfo, UserAdmin)