from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_title', 'course_core_technologies', 'course_level', 'course_upload_date')
    search_fields = ('course_title', 'course_core_technologies', 'course_level')
    list_filter = ('course_level',)
    ordering = ('-course_upload_date',)
    