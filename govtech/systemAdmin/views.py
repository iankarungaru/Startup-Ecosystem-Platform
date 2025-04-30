# sysadmin/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.models import User  # Import User model
from django.contrib.auth import login
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from .models import *
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from datetime import timedelta
from startup.helper import *
from django.core.mail import EmailMessage
from django.utils.crypto import get_random_string
from django.utils.timezone import now
from django.conf import settings

def index(request):
    # Explicitly specify the path to the template for sysadmin
    return render(request, 'auth/admin.html')
def authorize_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        ip = get_client_ip(request)

        # Get or create login attempt tracker
        attempt, created = LoginAttempt.objects.get_or_create(email=email, ip_address=ip)

        # Reset count if more than 10 minutes have passed
        if timezone.now() - attempt.last_attempt > timedelta(minutes=10):
            attempt.attempts = 0
            attempt.save()

        # Block login if locked out
        if attempt.attempts >= 5 and timezone.now() - attempt.last_attempt < timedelta(minutes=10):
            return JsonResponse(
                {'status': 'locked', 'message': 'Too many failed login attempts. Please try again in 10 minutes.'})



        try:
            # Get user by email
            user_obj = InternalUser.objects.get(email=email)

            if user_obj.isactive == 1:
                return JsonResponse({'status': 'error', 'message': 'Your account is deactivated/not activated. Please contact system admin.'})

            # Check password
            if not check_password(password, user_obj.password):
                attempt.attempts += 1
                attempt.last_attempt = timezone.now()
                attempt.save()
                return JsonResponse({'status': 'error', 'message': 'Invalid credentials.'})

            # Now get or create a Django User for authentication (temporary fix)
            # At this point, we’ve verified that the email and password match. Now, we need to create a Django User model (or get the existing one).
            # We use get_or_create to get the user based on the email (username in Django’s default User model). Since you are using a custom InternalUser model for authentication, we don’t use Django’s password system directly. Instead, we call set_unusable_password() to ensure no password is set on the User object.
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
            request.session['profile_picture'] = user_obj.profile_picture

            # Reset login attempts after successful login
            attempt.attempts = 0
            attempt.save()

            # update user ip address
            InternalUser.objects.filter(email=email).update(ip_address=ip)

            return JsonResponse({'status': 'success', 'message': 'Login successful.'})

        except InternalUser.DoesNotExist:
            attempt.attempts += 1
            attempt.last_attempt = timezone.now()
            attempt.save()
            return JsonResponse({'status': 'error', 'message': 'Invalid credentials.'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request.'})

def dashboard(request):
    return render(request, "pages/dashboard.html")