# sysadmin/views.py
import base64
import os
import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User  # Import User model
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from .models import *
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from datetime import timedelta
from startup.helper import *
from django.core.mail import EmailMultiAlternatives
from django.utils.crypto import get_random_string
from django.utils.timezone import now
from django.conf import settings
from dashboard.models import SignupUser

def index(request):
    # Explicitly specify the path to the template for sysadmin
    return render(request, 'auth/admin.html')
def authorize_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        ip = get_client_ip(request)

        # Get or create login attempt tracker
        attempt, created = AttemptLogin.objects.get_or_create(email=email, ip_address=ip)

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

def forgetPasswordSysAdmin(request):
    return render(request, 'auth/forgetPassword.html')

def verificationLinkSys(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        enteredEmail = email

        try:
            user = InternalUser.objects.get(email=email)
        except InternalUser.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Email does not exist in our system.'})

        # Check daily limit
        today_start = now().replace(hour=0, minute=0, second=0, microsecond=0)
        reset_count_today = PasswordResetToken.objects.filter(
            user=user,
            created_at__gte=today_start
        ).count()

        if reset_count_today >= 5:
            return JsonResponse({
                'status': 'error',
                'message': 'You have reached the daily password reset limit. Please try again tomorrow.'
            })

        # Generate OTP
        otp = get_random_string(length=8)

        # Save OTP to DB
        PasswordResetToken.objects.create(user=user, token=otp)

        subject = "System Administrator account Password Reset"
        from_email = f"Devlink System Admin Team <{settings.DEFAULT_FROM_EMAIL}>"

        # Plain text
        text_content = (
            f"You requested a password reset for your System Administrator account.\n\n"
            f"Your reset code is: {otp}\n\n"
            f"This code is valid for 10 minutes. If you did not request this, please ignore this message.\n\n"
            f"- Devlink Team"
        )

        # HTML content
        html_content = f"""
            <html>
            <body>
                <p>You requested a password reset for your <strong>System Administrator Account</strong> account.</p>
                <p><strong>Your reset code is:</strong> <code style="font-size: 18px;">{otp}</code></p>
                <p>This code is valid for 10 minutes. If you did not request this, you can safely ignore it.</p>
                <br>
                <p style="font-size: 14px; color: #888;">— Devlink Team</p>
            </body>
            </html>
        """

        # Send both plain text and HTML
        email_msg = EmailMultiAlternatives(subject, text_content, from_email, [email])
        email_msg.attach_alternative(html_content, "text/html")
        email_msg.send(fail_silently=False)

        return JsonResponse({
            'status': 'success',
            'message': 'An OTP has been sent to your email.',
            'email': enteredEmail,
        })

    return JsonResponse({'status': 'error', 'message': 'Invalid request.'})

def otpVerificationSys(request):
    return render(request,'auth/otp.html')

def verifyOTPSys(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        email = request.POST.get('email')

        if not email or not otp:
            return JsonResponse({'status': 'error', 'message': 'Missing email or OTP.'})

        try:
            user = InternalUser.objects.get(email=email)
        except InternalUser.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'User not found.'})

        # Get the most recent OTP/token for the user
        token_entry = PasswordResetToken.objects.filter(user=user).order_by('-created_at').first()

        if not token_entry:
            return JsonResponse({'status': 'error', 'message': 'No OTP found. Please request again.'})

        # Check OTP validity and expiration (e.g., 10 minutes)
        expiry_time = token_entry.created_at + timedelta(minutes=10)
        if token_entry.token == otp:
            if now() <= expiry_time:
                return JsonResponse({'status': 'success', 'message': 'OTP verified.'})
            else:
                return JsonResponse({'status': 'error', 'message': 'OTP has expired. Please request a new one.'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid OTP.'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

def ChangePasswordSys(request):
    return render(request,'auth/changePassword.html')

def saveForgetMyPasswordSys(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        new_password = request.POST.get('password')
        confirmpassword = request.POST.get('confirm_password')

        if new_password != confirmpassword:
            return JsonResponse({'status': 'warning', 'message': 'The new password and current password do not match.'})

        if not is_strong_password(new_password):
            return JsonResponse({'status': 'error', 'message': 'Password must be at least 8 characters long and include a capital letter, number, and symbol.'})

        # Encrypt the password
        encrypted_password = make_password(new_password)

        try:
            InternalUser.objects.filter(email=email).update(password=encrypted_password)
            return JsonResponse({'status': 'success', 'message': 'Password updated successfully.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Failed to update password: {str(e)}'})



    return JsonResponse({'status': 'error', 'message': 'Invalid request method or missing session ID.'})

def authlogoutSys(request):
    try:
        # Clear the session
        request.session.flush()

        # Logout the user
        logout(request)  # This will log the user out and clear their session.

        # You can return a success message via JSON if needed (optional)
        return redirect('/sysadmin/')  # Redirect to login page or other desired page

    except Exception as e:
        # Handle any errors that occur during logout
        return JsonResponse({'status': 'error', 'message': f'Error during logout: {str(e)}'})

def Adminprofile(request):
    myId = request.session.get('id')
    myInfo = InternalUser.objects.get(id=myId)
    data = {
        'firstName': myInfo.fName,
        'lastName': myInfo.lName,
        'email': myInfo.email,
        'phone': myInfo.phone,
        'nationality': getnationalityName(myInfo.nationality),
        'county': getCountyName(myInfo.county),
        'subcounty': getSubcountyName(myInfo.subcounty),
        'gender': getGenderName(myInfo.gender),
        'profilePicture': myInfo.profile_picture,
    }

    return render(request, 'pages/myprofile.html', data)

def profileChange(request):
    myId = request.session.get('id')
    myInfo = InternalUser.objects.get(id=myId)
    data = {
        'firstName': myInfo.fName,
        'lastName': myInfo.lName,
        'email': myInfo.email,
        'phone': myInfo.phone,
        'nationality': getnationalityName(myInfo.nationality),
        'nationalityId': myInfo.nationality,
        'county': getCountyName(myInfo.county),
        'countyId': myInfo.county,
        'subcounty': getSubcountyName(myInfo.subcounty),
        'subcountyId': myInfo.subcounty,
        'gender': getGenderName(myInfo.gender),
        'genderId': myInfo.gender,
        'countries': Country.objects.all().order_by('nationality'),
        'counties': County.objects.all().order_by('name'),
        'genders': gender.objects.all().order_by('name'),
    }

    return render(request, 'pages/editProfile.html', data)

def saveEditProfile(request):
    myId = request.session.get('id')

    if request.method == 'POST' and myId:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        nationality = request.POST.get('nationality')
        county = request.POST.get('county')
        subCounty = request.POST.get('subcounty')
        genderName = request.POST.get('gender')
        cropped_image_data = request.POST.get('cropped_image')  # Base64 string

        try:
            # Get existing user
            user = InternalUser.objects.get(id=myId)

            # Update fields
            user.fName = first_name
            user.lName = last_name
            user.email = email
            user.phone = phone
            user.nationality = nationality
            user.county = county
            user.subcounty = subCounty
            user.gender = genderName

            # Handle profile picture if provided
            if cropped_image_data and "base64" in cropped_image_data:
                format, imgstr = cropped_image_data.split(';base64,')
                ext = format.split('/')[-1]
                file_name = f"profile_{myId}_{uuid.uuid4().hex[:8]}.{ext}"

                # Define and create static/profiles/ directory
                static_profiles_dir = os.path.join(settings.BASE_DIR, 'static', 'profiles')
                os.makedirs(static_profiles_dir, exist_ok=True)

                file_path = os.path.join(static_profiles_dir, file_name)

                # Save the decoded image
                with open(file_path, "wb") as f:
                    f.write(base64.b64decode(imgstr))

                # Save relative path
                user.profile_picture = f"profiles/{file_name}"
                request.session['profile_picture'] = user.profile_picture

            # Save updated user (both with or without image)
            user.save()

            # Add notification
            title = "Editing of Profile"
            message = (
                "You have successfully updated your profile. "
                "Remember, updating your email or phone may affect your login credentials."
            )
            result = notification_insert(title, message, myId, sysNotification)
            if result['status'] != 'success':
                print("Notification insert failed:", result['message'])

            return JsonResponse({'status': 'success', 'message': 'Profile updated successfully'})

        except InternalUser.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'User not found.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Error updating profile: {e}'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method or missing session ID.'})

def resetPassword(request):
    return render(request, 'pages/myPassword.html')

def saveChangeMyPassword(request):
    myId = request.session.get('id')

    if request.method == 'POST' and myId:
        current_password = request.POST.get('currentPassword')
        # Get actual password in the db
        actualPassword = InternalUser.objects.filter(id=myId).values_list('password', flat=True).first()

        if not check_password(current_password, actualPassword):
            return JsonResponse({'status': 'warning', 'message': 'Invalid current password'})

        new_password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:
            return JsonResponse({'status': 'warning', 'message': 'The new password and current password do not match.'})

        if not is_strong_password(new_password):
            return JsonResponse({'status': 'error',
                                 'message': 'Password must be at least 8 characters long and include a capital letter, number, and symbol.'})

        # Encrypt the password
        encrypted_password = make_password(new_password)

        try:
            InternalUser.objects.filter(id=myId).update(password=encrypted_password)
            title = "Password Change"
            message = (
                "You have successfully updated your Account Password."
            )
            result = notification_insert(title, message, myId, sysNotification)
            if result['status'] != 'success':
                print("Notification insert failed:", result['message'])
            return JsonResponse({'status': 'success', 'message': 'Password updated successfully.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Failed to update password: {str(e)}'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method or missing session ID.'})

# let's start displaying notifications
def notifications(request):
    myId = request.session.get('id')
    notif = sysNotification.objects.filter(user_id=myId, is_read=False)

    data = {
        'notifications': [
            {
                'id': n.id,
                'title': n.title,
                'message': n.message,
                'is_read': n.is_read,
                'created_at': n.created_at,
                'accountName': getAccountNames(n.user_id),
            }
            for n in notif
        ]
    }
    return render(request, 'pages/viewNotification.html',data)

def markAsRead(request, pk):
    notification = get_object_or_404(sysNotification, pk=pk)
    notification.is_read = True
    notification.save()
    return redirect('Sys_notifications')  # or wherever you want to redirect

def viewMynotifications(request, pk):
    notification = get_object_or_404(sysNotification, pk=pk)

    # Optional: mark as read automatically on view
    if not notification.is_read:
        notification.is_read = True
        notification.save()

    return render(request, 'pages/view_notification.html', {
        'notification': notification
    })

def externalUsers(request):
    startupUsers = SignupUser.objects.values('id', 'fName', 'lName', 'email', 'phone', 'nationality','county', 'subcounty','gender', 'isactive', 'dateCreated')
    return render(request,'pages/externalUsers.html',{'startupUsers': startupUsers})

def internalUsers(request):
    icto = InternalUser.objects.values('id', 'fName', 'lName', 'idNo', 'email', 'phone', 'nationality','county', 'subcounty','gender', 'isactive', 'dateCreated')
    return render(request,'pages/internalUsers.html',{'internaluser': icto})

def internalUserSys(request):
    ictoSys = InternalUser.objects.values('id', 'fName', 'lName', 'idNo', 'email', 'phone', 'nationality','county', 'subcounty','gender', 'isactive', 'dateCreated')
    return render(request,'pages/internalUsers.html',{'internaluser': ictoSys})
