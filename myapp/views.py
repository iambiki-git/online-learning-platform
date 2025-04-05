from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

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
    
    


def courses_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    return render(request, 'myapp/courses.html')

def course_detail_view(request):
    return render(request, 'myapp/course_detail.html')


def lesson_page_view(request):
    return render(request, 'myapp/lesson_page.html')
