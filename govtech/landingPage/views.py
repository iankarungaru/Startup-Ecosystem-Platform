from django.shortcuts import render,redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from validate_email_address import validate_email
from django.contrib.auth.models import User  # Import User model
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from .models import *
import re
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError

def landing(request):
    return render(request, 'landing.html')

def register_view(request):
    countries = Country.objects.all().order_by('nationality')
    counties = County.objects.all().order_by('name')
    genders  = gender.objects.all().order_by('name')
    return render(request, 'register.html', {'countries': countries, 'counties': counties, 'genders':genders})

def get_subcounties(request):
    county_id = request.GET.get('county_id')
    subcounties = Subcounty.objects.filter(county_id=county_id).values('id', 'name')
    return JsonResponse(list(subcounties), safe=False)

# View for login page
def login_view(request):
    return render(request, 'login.html')

def is_strong_password(password):
    # At least 8 characters, one uppercase letter, one number, and one symbol
    return (
        len(password) >= 8 and
        re.search(r'[A-Z]', password) and
        re.search(r'[a-z]', password) and
        re.search(r'\d', password) and
        re.search(r'[^A-Za-z0-9]', password)
    )

def signup(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name') 
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')  
        phone = request.POST.get('phone')
        nationality = request.POST.get('nationality')  
        county = request.POST.get('county')
        subCounty = request.POST.get('subcounty')  
        genderName = request.POST.get('gender')
        password = request.POST.get('password')  
        confirm_password = request.POST.get('confirm_password')
        
        # Password match check
        if password != confirm_password:
            return JsonResponse({'status': 'error', 'message': 'Passwords do not match.'})
        
        # Password strength check
        if not is_strong_password(password):
            return JsonResponse({'status': 'error', 'message': 'Password must be at least 8 characters long and include a capital letter, number, and symbol.'})
        
        # Encrypt the password
        encrypted_password = make_password(password)
        
        # Save to DB
        try:
            user = SignupUser.objects.create(
                email=email,
                password=encrypted_password,
                fName=first_name,
                lName=last_name,
                phone=phone,
                nationality=nationality,
                county=county,
                subcounty=subCounty,
                gender=genderName
            )
            user.save()
            return JsonResponse({'status': 'success', 'message': 'Registration successful. Please log in.'})

        except IntegrityError:
            return JsonResponse({'status': 'error', 'message': 'An account with this email already exists.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'An error occurred while saving your data: {e}'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

def authlogin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            # Get user by email
            user = SignupUser.objects.get(email=email)

            # Check if the account is active (0 is active)
            if user.isactive == 1:
                return JsonResponse({'status': 'error', 'message': 'Your account is deactivated or not activated. Please contact system admin.'})
            
            # Validate password using check_password
            if not check_password(password, user.password):
                return JsonResponse({'status': 'error', 'message': 'Invalid credentials.'})  # Generic error message

            # Manually set session values
            request.session['user_id'] = user.id
            request.session['user_email'] = user.email

            return JsonResponse({'status': 'success', 'message': 'Login successful.'})

        except SignupUser.DoesNotExist:
            # Avoid exposing whether it's the email or password that is wrong
            return JsonResponse({'status': 'error', 'message': 'Invalid credentials.'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request.'})
