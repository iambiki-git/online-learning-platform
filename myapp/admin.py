from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_title', 'course_core_technologies', 'course_level', 'course_upload_date')
    search_fields = ('course_title', 'course_core_technologies', 'course_level')
    list_filter = ('course_level',)
    ordering = ('-course_upload_date',)


@admin.register(CourseDetail)
class CourseDetailAdmin(admin.ModelAdmin):
    list_display = ('course', 'course_description', 'about_couse', 'what_you_will_learn')
    search_fields = ('course__course_title',)
    list_filter = ('course',)
    ordering = ('-course__course_upload_date',)
    

@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ('chapter_title', 'course', 'chapter_upload_date')
    search_fields = ('chapter_title', 'course__course_title')
    list_filter = ('course',)
    ordering = ('-chapter_upload_date',)


@admin.register(ChapterDetail)
class ChapterDetailAdmin(admin.ModelAdmin):
    list_display = ('chapter', 'features', 'advantages', 'disadvantages')
    search_fields = ('chapter__chapter_title',)
    list_filter = ('chapter',)
    ordering = ('-chapter__chapter_upload_date',)