from django.db import models

# Create your models here.

class Course(models.Model):
    course_title = models.CharField(max_length=255, blank=True, null=True)
    course_core_technologies = models.CharField(max_length=255, blank=True, null=True)
    course_level = models.CharField(max_length=50, blank=True, null=True)
    course_description = models.TextField(blank=True, null=True)
    about_couse = models.TextField(blank=True, null=True)
    what_you_will_learn = models.TextField(blank=True, null=True)
    contributors = models.TextField(blank=True, null=True)
    course_image = models.ImageField(upload_to='course_images/', blank=True, null=True)
    course_upload_date = models.DateTimeField(auto_now_add=True)
    course_update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.course_title if self.course_title else "Course Title Not Provided"
    
