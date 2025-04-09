from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import *

# Create your views here.

def home(request):
    return render(request, 'myapp/home.html')



def registration_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == "POST":
        # Handle form submission for registration
        full_name = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip().lower()  # Normalize email
        password = request.POST.get('password', '').strip()

        # Validation checks
        errors = False
        
        # Check required fields
        if not all([full_name, email, password]):
            messages.error(request, 'All fields are required')
            errors = True
        
        form_data = {
            'full_name':full_name,
            'email': email,    
          # Don't preserve password for security
        }

        # Validate full name
        if full_name:
            # Check if name contains at least one space (first and last name)
            if len(full_name.split()) < 2:
                messages.error(request, 'Please enter both first and last name')
                errors = True
            
            # Check for invalid characters (allowing spaces and hyphens)
            if not all(c.isalpha() or c.isspace() or c == '-' for c in full_name):
                messages.error(request, 'Name can only contain letters, spaces, and hyphens')
                errors = True
        
        # Validate email
        if email:
            try:
                validate_email(email)
            except ValidationError:
                messages.error(request, 'Invalid email address')
                errors = True
            else:
                if User.objects.filter(email__iexact=email).exists():
                    messages.error(request, 'Email already exists')
                    errors = True
        
        # Validate password
        if password:
            if len(password) < 8:  # More secure minimum length
                messages.error(request, 'Password must be at least 8 characters long')
                errors = True
            
            # More comprehensive password validation
            has_upper = any(c.isupper() for c in password)
            has_lower = any(c.islower() for c in password)
            has_digit = any(c.isdigit() for c in password)
            has_special = any(c in "!@#$%^&*()-_+=<>?/{}[]|:;'" for c in password)
            
            if not (has_upper and has_lower and has_digit and has_special):
                messages.error(request, 
                    'Password must contain at least: '
                    '1 uppercase letter, 1 lowercase letter, '
                    '1 digit, and 1 special character'
                )
                errors = True
        
        if errors:
            return render(request, 'myapp/register.html', {'form_data': form_data})
        
        # Create user
        try:
            # Split name into first and last
            name_parts = full_name.split()
            first_name = name_parts[0]
            last_name = ' '.join(name_parts[1:]) if len(name_parts) > 1 else ''
            
            user = User.objects.create_user(
                username=email,  # Using email as username
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('login')  # Redirect to login page
            
        except Exception as e:
            messages.error(request, f'Error creating account: {str(e)}')
            return render(request, 'myapp/register.html', {'form_data': form_data})
    
    return render(request, 'myapp/register.html')


from django.contrib.auth import login

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '').strip()
        remember_me = bool(request.POST.get('remember_me', False))

        # Preserve form data in case of errors
        form_data = {
            'email': email,
            'remember_me': remember_me,
            # Don't preserve password for security
        }

        # Basic validation
        if not email or not password:
            messages.error(request, 'Email and password are required')
            return render(request, 'myapp/login.html', {'form_data': form_data})

        try:
            user = User.objects.get(email__iexact=email)
            if user.check_password(password):
                login(request, user)
                request.session.set_expiry(1209600 if remember_me else 0)  # 2 weeks or browser session
                # messages.success(request, 'Login successful!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid email or password')
        except User.DoesNotExist:
            messages.error(request, 'Invalid email or password')

        return render(request, 'myapp/login.html', {'form_data': form_data})
    
    # GET request
    return render(request, 'myapp/login.html')


from django.contrib.auth import logout
def logout_view(request):
    # Handle logout
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('login')  # Redirect to login page
    
    

from django.db.models import Count
def courses_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Fetch courses and annotate with chapter count
    courses = Course.objects.annotate(chapter_count=Count('chapters'))

    
    # Check if there are any courses
    if not courses:
        messages.info(request, 'No courses available at the moment.')
        return render(request, 'myapp/courses.html')
    
    # Pass the courses to the template
    content = {
        'courses':courses,
    }

    return render(request, 'myapp/courses.html', content)



def course_detail_view(request, course_id):
    if not request.user.is_authenticated:
        return redirect('login')
    
    try:
        course = Course.objects.get(id=course_id)
        contributors = course.course_detail.contributors
        chapters = course.chapters.all()
        chapter_count = course.chapters.count()
        course_highlights = course.course_detail.what_you_will_learn.strip().split('\n')
    except Course.DoesNotExist:
        messages.error(request, 'Course not found')
        return redirect('courses')
    
    context = {
        'course': course,
        'chapters':chapters,
        'chapter_count':chapter_count,
        'highlights':course_highlights,
        'contributors':contributors,
    }
    return render(request, 'myapp/course_detail.html', context)



import markdown
def lesson_page_view(request, course_id):
    if not request.user.is_authenticated:
        return redirect('login')
    
   
    course = Course.objects.get(id=course_id)
    chapters = course.chapters.filter(course=course)  # Fetch chapters related to the course    

    context = {
        'course': course,
        'chapters': chapters,
    }

    return render(request, 'myapp/lesson_page.html', context)



from django.http import JsonResponse
from .models import Chapter

def get_chapter_content(request, chapter_id):
    try:
        chapter = Chapter.objects.get(id=chapter_id)
        content = chapter.chapter_detail.description  # Assuming you have a `content` field in the `Chapter` model
        chapter_title = chapter.chapter_title  # Get the chapter title

        previous_chapter = Chapter.objects.filter(id__lt=chapter_id).order_by('-id').first()
        next_chapter = Chapter.objects.filter(id__gt=chapter_id).order_by('id').first()       


        # Convert Markdown to HTML
        description_html = markdown.markdown(content, extensions=['fenced_code', 'codehilite', 'nl2br'])
        
        # If you're receiving raw text, convert \n to <br> or wrap in <p> tags
        description = description_html.replace('\r\n', '<br>').replace('\n', '<br>')

        return JsonResponse({
            'content': description, 
            'title': chapter_title,
            'previous_chapter_id': previous_chapter.id if previous_chapter else None,
            'next_chapter_id': next_chapter.id if next_chapter else None,
            

            
            })
    except Chapter.DoesNotExist:
        return JsonResponse({'error': 'Chapter not found'}, status=404)
