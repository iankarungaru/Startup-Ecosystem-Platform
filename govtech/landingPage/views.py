from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User  # Import User model
from django.core.mail import EmailMultiAlternatives
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.crypto import get_random_string
from django.utils.timezone import now

from startup.helper import *
from .models import *
from dashboard.models import Notification


def landing(request):
    return render(request, 'landing.html')


def register_view(request):
    countries = Country.objects.all().order_by('nationality')
    counties = County.objects.all().order_by('name')
    genders = gender.objects.all().order_by('name')
    return render(request, 'register.html', {'countries': countries, 'counties': counties, 'genders': genders})


def get_subcounties(request):
    county_id = request.GET.get('county_id')
    subcounties = Subcounty.objects.filter(county_id=county_id).values('id', 'name')
    return JsonResponse(list(subcounties), safe=False)


# View for login page
def login_view(request):
    return render(request, 'login.html')


def signup(request):
    if request.method == 'POST':
        account_type = request.POST.get('account_type')  # '1' for individual, '2' for company

        # Initialize fields
        first_name = ''
        last_name = ''
        company_name = ''
        genderName = None
        nationality = None

        # Individual details
        if account_type == '1':
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            genderName = request.POST.get('gender')
            nationality = request.POST.get('nationality')
        else:
            company_name = request.POST.get('company_name')
            nationality = 73  # Default for companies

        # Common details
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        county = request.POST.get('county')
        subCounty = request.POST.get('subcounty')

        # Password generation and encryption
        password = generate_strong_password()
        encrypted_password = make_password(password)

        try:
            # Save user to DB
            user = SignupUser.objects.create(
                email=email,
                password=encrypted_password,
                fName=first_name,
                lName=last_name,
                phone=phone,
                nationality=nationality,
                county=county,
                subcounty=subCounty,
                gender=genderName,
                accountType=account_type,
                company=company_name
            )

            # Add notification
            title = "Account created successfully"
            message = (
                "You have successfully created your account. "
                "Proceed to make the relevant applications."
            )
            result = notification_insert(title, message, user.id, Notification)
            if result['status'] != 'success':
                print("Notification insert failed:", result['message'])

            # Prepare email
            subject = "Your Devlink Platform Account Details"
            from_email = f"Devlink Team <{settings.DEFAULT_FROM_EMAIL}>"

            # Plain text content
            text_content = (
                f"Dear User,\n\n"
                f"Your account on the Devlink Startup Ecosystem Platform has been created successfully.\n\n"
                f"Here are your login credentials:\n"
                f"Email: {email}\n"
                f"Password: {password}\n\n"
                f"For security, please log in and change your password as soon as possible.\n\n"
                f"Regards,\n"
                f"The Devlink Team"
            )

            # HTML content
            html_content = f"""
                <html>
                <body>
                    <p>Dear User,</p>
                    <p>Your account on the <strong>Devlink Startup Ecosystem Platform</strong> has been created successfully.</p>
                    <p><strong>Your login credentials are:</strong></p>
                    <ul>
                        <li><strong>Email:</strong> {email}</li>
                        <li><strong>Password:</strong> <code style="font-size: 16px;">{password}</code></li>
                    </ul>
                    <p>For your security, please log in and change your password as soon as possible.</p>
                    <br>
                    <p style="font-size: 14px; color: #888;">— The Devlink Team</p>
                </body>
                </html>
            """

            # Send email
            email_msg = EmailMultiAlternatives(subject, text_content, from_email, [email])
            email_msg.attach_alternative(html_content, "text/html")
            email_msg.send(fail_silently=False)

            return JsonResponse({
                'status': 'success',
                'message': 'Registration successful. Login credentials have been sent to your email.'
            })

        except IntegrityError:
            return JsonResponse({'status': 'error', 'message': 'An account with this email already exists.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Error occurred: {e}'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})


def authlogin(request):
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
            user_obj = SignupUser.objects.get(email=email)

            if user_obj.isactive == 1:
                return JsonResponse({'status': 'error',
                                     'message': 'Your account is deactivated or not activated. Please contact system admin.'})

            # Check password
            if not check_password(password, user_obj.password):
                attempt.attempts += 1
                attempt.last_attempt = timezone.now()
                attempt.save()
                return JsonResponse({'status': 'error', 'message': 'Invalid credentials.'})

                # ✅ Check if password change is required
            if user_obj.pswdchange == 1:
                return JsonResponse({
                    'status': 'force_change',
                    'message': 'You are required to change your password.',
                    'user_id': user_obj.id,
                    'user_email': user_obj.email
                })

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

            if user_obj.accountType == 1:
                request.session['fName'] = user_obj.fName
                request.session['lName'] = user_obj.lName
            else:
                request.session['company'] = user_obj.company

            request.session['email'] = user_obj.email
            request.session['profile_picture'] = user_obj.profile_picture
            request.session['userType'] = user_obj.accountType

            # Reset login attempts after successful login
            attempt.attempts = 0
            attempt.save()

            # update user ip address
            SignupUser.objects.filter(email=email).update(ip_address=ip)

            return JsonResponse({'status': 'success', 'message': 'Login successful.'})

        except SignupUser.DoesNotExist:
            attempt.attempts += 1
            attempt.last_attempt = timezone.now()
            attempt.save()
            return JsonResponse({'status': 'error', 'message': 'Invalid credentials.'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request.'})


def forgetPassword(request):
    return render(request, 'forgetPassword.html')


def verificationLink(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        enteredEmail = email

        try:
            user = SignupUser.objects.get(email=email)
        except SignupUser.DoesNotExist:
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

        subject = "Startup Ecosystem Platform account Password Reset"
        from_email = f"Devlink Team <{settings.DEFAULT_FROM_EMAIL}>"

        # Plain text
        text_content = (
            f"You requested a password reset for your Startup Ecosystem Platform account.\n\n"
            f"Your reset code is: {otp}\n\n"
            f"This code is valid for 10 minutes. If you did not request this, please ignore this message.\n\n"
            f"- Devlink Team"
        )

        # HTML content
        html_content = f"""
            <html>
            <body>
                <p>You requested a password reset for your <strong>Startup Ecosystem Platform account</strong> account.</p>
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


def otpVerification(request):
    return render(request, 'otp.html')


def verifyOTP(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        email = request.POST.get('email')

        if not email or not otp:
            return JsonResponse({'status': 'error', 'message': 'Missing email or OTP.'})

        try:
            user = SignupUser.objects.get(email=email)
        except SignupUser.DoesNotExist:
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


def ChangePassword(request):
    return render(request, 'changePassword.html')


def saveForgetMyPassword(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = SignupUser.objects.get(email=email)
        myId = user.id

        new_password = request.POST.get('password')
        confirmpassword = request.POST.get('confirm_password')

        if new_password != confirmpassword:
            return JsonResponse({'status': 'warning', 'message': 'The new password and current password do not match.'})

        if not is_strong_password(new_password):
            return JsonResponse({'status': 'error',
                                 'message': 'Password must be at least 8 characters long and include a capital letter, number, and symbol.'})

        # Encrypt the password
        encrypted_password = make_password(new_password)

        try:
            SignupUser.objects.filter(email=email).update(password=encrypted_password)
            title = "Forgot Password Change"
            message = (
                "You have successfully updated your Account Password."
            )
            result = notification_insert(title, message, myId, Notification)
            if result['status'] != 'success':
                print("Notification insert failed:", result['message'])
            return JsonResponse({'status': 'success', 'message': 'Password updated successfully.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Failed to update password: {str(e)}'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method or missing session ID.'})


def force_password_change(request):
    email = request.GET.get('email')
    userId = request.GET.get('userId')
    return render(request, 'changeForcePassword.html', {'user_id': userId, 'email': email})


def saveForgetMyPasswordForce(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        myId = request.POST.get('myId')
        new_password = request.POST.get('password')
        confirmpassword = request.POST.get('confirm_password')

        if new_password != confirmpassword:
            return JsonResponse({'status': 'warning', 'message': 'The new password and current password do not match.'})

        if not is_strong_password(new_password):
            return JsonResponse({'status': 'error',
                                 'message': 'Password must be at least 8 characters long and include a capital letter, number, and symbol.'})

        # Encrypt the password
        encrypted_password = make_password(new_password)

        try:
            SignupUser.objects.filter(email=email).update(password=encrypted_password, pswdchange=0)
            title = "Update Forgot Password Force"
            message = (
                "You have successfully updated your Account Password."
            )
            result = notification_insert(title, message, myId, Notification)
            if result['status'] != 'success':
                print("Notification insert failed:", result['message'])
            return JsonResponse({'status': 'success', 'message': 'Password updated successfully.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Failed to update password: {str(e)}'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method or missing session ID.'})
