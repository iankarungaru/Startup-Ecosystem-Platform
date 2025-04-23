from django.contrib.auth import logout
from django.http import HttpResponse
from django.http import JsonResponse
from django.urls import reverse
from landingPage.models import SignupUser, County, Subcounty, Country, gender
from startup.helper import *
import os, uuid, base64
from django.conf import settings
from django.shortcuts import render
from .models import Registration, IndividualDev
from django.db.models import Count
from django.utils.safestring import mark_safe
import json
from datetime import date


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

from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Registration
from .forms import Step1Form, Step2Form  # You'll need to create these forms
from django.contrib import messages

def multi_step_registration(request, step):
    step = int(step)

    if step == 1:
        if request.method == 'POST':
            form = Step1Form(request.POST)
            if form.is_valid():
                step1_data = form.cleaned_data.copy()
                
                # Convert date to string
                if isinstance(step1_data.get('date_of_establishment'), date):
                    step1_data['date_of_establishment'] = step1_data['date_of_establishment'].isoformat()

                request.session['step1_data'] = step1_data
                return redirect('multi_step', step=2)
        else:
            form = Step1Form()
        return render(request, 'register/step1.html', {'form': form, 'step': step})

    elif step == 2:
        if request.method == 'POST':
            form = Step2Form(request.POST)
            if form.is_valid():
                step1_data = request.session.get('step1_data')
                if not step1_data:
                    messages.error(request, "Step 1 data not found. Please start again.")
                    return redirect('multi_step', step=1)

                # Convert date string back to date object
                if 'date_of_establishment' in step1_data:
                    step1_data['date_of_establishment'] = date.fromisoformat(step1_data['date_of_establishment'])

                all_data = {**step1_data, **form.cleaned_data}
                Registration.objects.create(**all_data)

                # Clean up session
                del request.session['step1_data']
                messages.success(request, "Registration complete!")
                return redirect('dashboard_view')  # Optional success page
        else:
            form = Step2Form()
        return render(request, 'register/step2.html', {'form': form, 'step': step})

from django.shortcuts import render, redirect
from .forms import IndividualForm


def individual_reg(request):
    if request.method == 'POST':
        form = IndividualForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard_view')  # Optional success page
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

def dashboard_view(request):
    total_companies = Registration.objects.count()
    total_individuals = IndividualDev.objects.count()

    company_nature = Registration.objects.values('nature').annotate(count=Count('nature'))
    business_model = Registration.objects.values('business_model').annotate(count=Count('business_model'))
    stage = Registration.objects.values('stage').annotate(count=Count('stage'))

    establishment_years = Registration.objects.dates('date_of_establishment', 'year')
    year_counts = {year.year: Registration.objects.filter(date_of_establishment__year=year.year).count() for year in establishment_years}

    context = {
        'total_companies': total_companies,
        'total_individuals': total_individuals,
        'company_nature_labels': mark_safe(json.dumps([entry['nature'] for entry in company_nature])),
        'company_nature_data': mark_safe(json.dumps([entry['count'] for entry in company_nature])),
        'business_model_labels': mark_safe(json.dumps([entry['business_model'] for entry in business_model])),
        'business_model_data': mark_safe(json.dumps([entry['count'] for entry in business_model])),
        'stage_labels': mark_safe(json.dumps([entry['stage'] for entry in stage])),
        'stage_data': mark_safe(json.dumps([entry['count'] for entry in stage])),
        'year_labels': mark_safe(json.dumps(list(year_counts.keys()))),
        'year_data': mark_safe(json.dumps(list(year_counts.values()))),
    }

    return render(request, 'dashboard.html', context)

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
