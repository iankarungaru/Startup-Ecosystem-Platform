from django.shortcuts import render,redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from validate_email_address import validate_email
from django.contrib.auth.models import User  # Import User model
from django.contrib.auth import authenticate, login
from .models import *
# from landingPage.models import CustomUser  # Import your custom model  # Import authenticate and login

# Create your views here.
def landing(request):
    return render(request, 'landing.html')

from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
# from landingPage.models import CustomUser

def register_view(request):
    countries = Country.objects.all().order_by('nationality')
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        nationality = request.POST.get('nationality')
        county = request.POST.get('county')
        subcounty = request.POST.get('subcounty')
        gender = request.POST.get('gender')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'register.html')

        # Check if email is already registered
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email is already registered.')
            return render(request, 'register.html')

        # Create the user
        try:
            user = CustomUser.objects.create_user(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                nationality=nationality,
                county=county,
                subcounty=subcounty,
                gender=gender
            )
            user.save()

            # Send verification email
            verification_link = 'http://your-domain.com/verify/'
            send_mail(
                'Email Verification',
                f'Hi {first_name}, Welcome to Startup Kenya! Click the link to verify your email: {verification_link}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )

            messages.success(request, 'Registration successful! A verification email has been sent.')
            return redirect('dashboard:dashboard')

        except Exception as e:
            messages.error(request, f'An error occurred: {e}')
            return render(request, 'register.html')
        
        
        

    return render(request, 'register.html',{'countries': countries})


# View for login page
def login_view(request):
    return render(request, 'login.html')

def authlogin(request):
    if request.method == 'POST':
        # Get form data
        email = request.POST.get('email')  # Adjust field names as per your form
        password = request.POST.get('password')
        print(f"Email: {email}, Password: {password}")  # Debug
        
        # Authenticate user (assuming you're using Django's auth system)
        user = authenticate(request, username=email, password=password)
        print(f"User: {user}")  # Debug
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('dashboard:dashboard')  # Replace 'home' with your desired redirect URL
        else:
            messages.error(request, 'Invalid email or password.')
            return render(request, 'login.html')
    
    # For GET requests, show the login form
    return render(request, 'login.html')


    