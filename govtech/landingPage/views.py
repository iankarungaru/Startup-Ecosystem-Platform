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
            user_obj = SignupUser.objects.get(email=email)

            if user_obj.isactive == 1:
                return JsonResponse({'status': 'error', 'message': 'Your account is deactivated or not activated. Please contact system admin.'})

            # Check password
            if not check_password(password, user_obj.password):
                return JsonResponse({'status': 'error', 'message': 'Invalid credentials.'})

            # Now get or create a Django User for authentication (temporary fix)
            # At this point, we’ve verified that the email and password match. Now, we need to create a Django User model (or get the existing one).
            # We use get_or_create to get the user based on the email (username in Django’s default User model). Since you are using a custom SignupUser model for authentication, we don’t use Django’s password system directly. Instead, we call set_unusable_password() to ensure no password is set on the User object.
            # Finally, we save the User model to the database. We are doing this to enforce the login required middleware
            user, created = User.objects.get_or_create(username=user_obj.email)
            user.set_unusable_password()  # since we’re not using Django’s password system
            user.save()

            # Log the user in properly
            login(request, user)

            # Set the user details in the session (id, email, fName, lName)
            request.session['id'] = user_obj.id
            request.session['email'] = user_obj.email
            request.session['fName'] = user_obj.fName
            request.session['lName'] = user_obj.lName

            # Debugging: Print session data
            print(f"Session set: {request.session.items()}")  # Print the session data to check if it's being set

            return JsonResponse({'status': 'success', 'message': 'Login successful.'})

        except SignupUser.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Invalid credentials.'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request.'})
