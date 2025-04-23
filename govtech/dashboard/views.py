from django.contrib.auth import logout
from django.http import HttpResponse
from django.http import JsonResponse
from django.urls import reverse
from landingPage.models import SignupUser, County, Subcounty, Country, gender
from startup.helper import *
import os, uuid, base64
from django.conf import settings
from django.contrib.auth.hashers import check_password, make_password
from .forms import (
    Step1Form, Step2Form
)
from .models import Registration


def dashboard_data(request):
    return render(request, "dashboard.html")


def index(request):
    return render(request, "index.html")


def get_form(step):
    forms = {
        1: Step1Form,
        2: Step2Form,
    }
    return forms.get(step)


from datetime import date


def multi_step_registration(request, step=1):
    step = int(step)
    form_class = get_form(step)

    if not form_class:
        return HttpResponse("Invalid step.")

    if request.method == "POST":
        form = form_class(request.POST, request.FILES)
        if form.is_valid():
            form_data = form.cleaned_data

            # Convert date fields to string format
            if "date_of_establishment" in form_data and isinstance(form_data["date_of_establishment"], date):
                form_data["date_of_establishment"] = form_data["date_of_establishment"].isoformat()

            # Handle file uploads by storing only file names in the session
            if "company_logo" in form_data and form_data["company_logo"]:
                file = form_data.pop("company_logo")  # Remove file from session data
                file_path = f'logos/{file.name}'  # Define file path
                with open(f'media/{file_path}', 'wb+') as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)
                form_data["company_logo"] = file_path  # Store only file path in session

            if "business_certificate" in request.FILES:
                file = request.FILES["business_certificate"]
                file_path = f'logos/{file.name}'  # Define file path
                with open(f'media/{file_path}', 'wb+') as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)
                form_data["business_certificate"] = file_path  # Store file path instead of file object

            request.session[f'step_{step}'] = form_data

            next_step = step + 1
            if next_step > 2:
                return redirect(reverse("registration_complete"))
            return redirect(reverse("multi_step", kwargs={"step": next_step}))

    else:
        initial_data = request.session.get(f'step_{step}', {})
        if "date_of_establishment" in initial_data:
            try:
                initial_data["date_of_establishment"] = date.fromisoformat(initial_data["date_of_establishment"])
            except ValueError:
                pass

        form = form_class(initial=initial_data)

    return render(request, f"register/step{step}.html", {"form": form, "step": step})


def registration_complete(request):
    # Combine session data from step 1 and 2
    data = {}
    for i in range(1, 3):
        step_data = request.session.get(f'step_{i}', {})
        data.update(step_data)

    # Convert date back to Python date object
    if "date_of_establishment" in data and isinstance(data["date_of_establishment"], str):
        try:
            data["date_of_establishment"] = date.fromisoformat(data["date_of_establishment"])
        except ValueError:
            data["date_of_establishment"] = None

    # Save to the Registration model
    Registration.objects.create(**data)

    # Clear session data
    for i in range(1, 3):
        request.session.pop(f'step_{i}', None)

    return render(request, "dashboard.html")


from django.shortcuts import render, redirect
from .forms import IndividualForm


def individual_reg(request):
    if request.method == 'POST':
        form = IndividualForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "dashboard.html")  # Adjust URL as needed
    else:
        form = IndividualForm()

    return render(request, "register/individual.html", {'form': form})


def authlogout(request):
    try:
        # Clear the session
        request.session.flush()

        # Logout the user
        logout(request)  # This will log the user out and clear their session.

        # You can return a success message via JSON if needed (optional)
        return redirect('/login/')  # Redirect to login page or other desired page

    except Exception as e:
        # Handle any errors that occur during logout
        return JsonResponse({'status': 'error', 'message': f'Error during logout: {str(e)}'})


def Myprofile(request):
    myId = request.session.get('id')
    myInfo = SignupUser.objects.get(id=myId)
    data = {
        'firstName': myInfo.fName,
        'lastName': myInfo.lName,
        'email': myInfo.email,
        'phone': myInfo.phone,
        'nationality': getnationalityName(myInfo.nationality),
        'county': getCountyName(myInfo.county),
        'subcounty': getSubcountyName(myInfo.subcounty),
        'gender': getGenderName(myInfo.gender),
        'profilePicture':myInfo.profile_picture,
    }

    return render(request, 'myprofile.html', data)


def profileChange(request):
    myId = request.session.get('id')
    myInfo = SignupUser.objects.get(id=myId)
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
        'genderId':myInfo.gender,
        'countries': Country.objects.all().order_by('nationality'),
        'counties': County.objects.all().order_by('name'),
        'genders': gender.objects.all().order_by('name'),
    }

    return render(request, 'editProfile.html', data)

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
        cropped_image_data = request.POST.get('cropped_image')  # Get cropped base64 string

        try:
            # Get existing user
            user = SignupUser.objects.get(id=myId)

            # Update fields
            user.fName = first_name
            user.lName = last_name
            user.email = email
            user.phone = phone
            user.nationality = nationality
            user.county = county
            user.subcounty = subCounty
            user.gender = genderName

            # Save profile picture if provided
            if cropped_image_data and "base64" in cropped_image_data:
                format, imgstr = cropped_image_data.split(';base64,')
                ext = format.split('/')[-1]
                file_name = f"profile_{myId}_{uuid.uuid4().hex[:8]}.{ext}"

                # Define static/profiles/ directory
                static_profiles_dir = os.path.join(settings.BASE_DIR, 'static', 'profiles')
                os.makedirs(static_profiles_dir, exist_ok=True)  # Ensure directory exists

                file_path = os.path.join(static_profiles_dir, file_name)

                # Write image to file
                with open(file_path, "wb") as f:
                    f.write(base64.b64decode(imgstr))

                # Save relative path in DB (to be used with {% static %})
                user.profile_picture = f"profiles/{file_name}"
                request.session['profile_picture'] = user.profile_picture

            user.save()
            return JsonResponse({'status': 'success', 'message': 'Profile updated successfully'})

        except SignupUser.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'User not found.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Error updating profile: {e}'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method or missing session ID.'})

def mySupport(request):
    return render(request,'support.html')

def resetPassword(request):
    return render(request,'myPassword.html')

def saveChangeMyPassword(request):
    myId = request.session.get('id')

    if request.method == 'POST' and myId:
        current_password = request.POST.get('currentPassword')
        # Get actual password in the db
        actualPassword = SignupUser.objects.filter(id=myId).values_list('password', flat=True).first()

        if not check_password(current_password, actualPassword):
            return JsonResponse({'status': 'warning', 'message': 'Invalid current password'})

        new_password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:
            return JsonResponse({'status': 'warning', 'message': 'The new password and current password do not match.'})

        if not is_strong_password(new_password):
            return JsonResponse({'status': 'error', 'message': 'Password must be at least 8 characters long and include a capital letter, number, and symbol.'})

        # Encrypt the password
        encrypted_password = make_password(new_password)

        try:
            SignupUser.objects.filter(id=myId).update(password=encrypted_password)
            return JsonResponse({'status': 'success', 'message': 'Password updated successfully.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Failed to update password: {str(e)}'})



    return JsonResponse({'status': 'error', 'message': 'Invalid request method or missing session ID.'})
