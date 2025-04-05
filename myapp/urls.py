from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('register/', registration_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('courses/', courses_view, name='courses'),
    path('course-detail/', course_detail_view, name='course_detail'),
    path('lesson-page/', lesson_page_view, name='lesson_page'),
]
