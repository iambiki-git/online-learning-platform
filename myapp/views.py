from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'myapp/home.html')

def registration_view(request):
    return render(request, 'myapp/register.html')

def login_view(request):
    return render(request, 'myapp/login.html') 

def courses_view(request):
    return render(request, 'myapp/courses.html')

def course_detail_view(request):
    return render(request, 'myapp/course_detail.html')