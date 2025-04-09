from django.db import models

# Create your models here.

class Course(models.Model):
    course_title = models.CharField(max_length=255, blank=True, null=True)
    course_core_technologies = models.CharField(max_length=255, blank=True, null=True)
    course_level = models.CharField(max_length=50, blank=True, null=True)
    course_upload_date = models.DateTimeField(auto_now_add=True)
    course_update_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.course_title if self.course_title else "Course Title Not Provided"
    
class CourseDetail(models.Model):
    course = models.OneToOneField(Course, related_name='course_detail', on_delete=models.CASCADE)
    course_description = models.TextField(blank=True, null=True)
    about_couse = models.TextField(blank=True, null=True)
    what_you_will_learn = models.TextField(blank=True, null=True)
    contributors = models.TextField(blank=True, null=True)
    course_image = models.ImageField(upload_to='course_images/', blank=True, null=True)

    def __str__(self):
        return f"Course Detail for {self.course.course_title}" if self.course.course_title else "Course Detail Not Provided"



class Chapter(models.Model):
    course = models.ForeignKey(Course, related_name='chapters', on_delete=models.CASCADE)
    chapter_title = models.CharField(max_length=255, blank=True, null=True)
    chapter_upload_date = models.DateTimeField(auto_now_add=True)
    chapter_update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.chapter_title if self.chapter_title else "Chapter Title Not Provided"
    
class ChapterDetail(models.Model):
    chapter = models.OneToOneField(Chapter, related_name='chapter_detail', on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    example_image = models.ImageField(upload_to='example_images/', blank=True, null=True)


    def __str__(self):
        return f"Chapter Detail for {self.chapter.chapter_title}" if self.chapter.chapter_title else "Chapter Detail Not Provided"
    