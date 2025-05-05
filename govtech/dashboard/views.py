import base64
import json
import os
import uuid
from calendar import month_name
from datetime import date

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.hashers import check_password, make_password
from django.db.models import Count
from django.db.models.functions import ExtractMonth
from django.db.models.functions import ExtractYear
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.safestring import mark_safe

from startup.helper import *
from .forms import IndividualForm
from .forms import Step1Form, Step2Form  # You'll need to create these forms
from .models import Registration, IndividualDev


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
        'profilePicture': myInfo.profile_picture,
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
        'genderId': myInfo.gender,
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
        cropped_image_data = request.POST.get('cropped_image')  # Base64 string

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
            result = notification_insert(title, message, myId, Notification)
            if result['status'] != 'success':
                print("Notification insert failed:", result['message'])

            return JsonResponse({'status': 'success', 'message': 'Profile updated successfully'})

        except SignupUser.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'User not found.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Error updating profile: {e}'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method or missing session ID.'})



def mySupport(request):
    return render(request, 'support.html')


def resetPassword(request):
    return render(request, 'myPassword.html')


def dashboard_view(request):
    # Basic totals
    total_companies = Registration.objects.count()
    total_individuals = IndividualDev.objects.count()

    # Pie/Bar/Doughnut chart data
    company_nature = Registration.objects.values('nature').annotate(count=Count('nature'))
    business_model = Registration.objects.values('business_model').annotate(count=Count('business_model'))
    stage = Registration.objects.values('stage').annotate(count=Count('stage'))

    # Line chart: Companies by year
    establishment_years = Registration.objects.dates('date_of_establishment', 'year')
    year_counts = {
        year.year: Registration.objects.filter(date_of_establishment__year=year.year).count()
        for year in establishment_years
    }

    # Monthly registration data for comparison
    def monthly_data_for_year(year):
        monthly_counts = (
            Registration.objects.filter(date_of_establishment__year=year)
            .annotate(month=ExtractMonth('date_of_establishment'))
            .values('month')
            .annotate(count=Count('id'))
        )
        month_data = {entry['month']: entry['count'] for entry in monthly_counts}
        return [month_data.get(i, 0) for i in range(1, 13)]

    # Set your desired years for comparison (can be dynamic)
    available_years = range(2020, 2025)
    all_years_data = {
        str(year): monthly_data_for_year(year) for year in available_years
    }

    # Month labels (Jan–Dec)
    month_labels = [month_name[i] for i in range(1, 13)]

    years_qs = (Registration.objects
                .annotate(year=ExtractYear('date_of_establishment'))
                .values_list('year', flat=True)
                .distinct()
                .order_by('-year')[:10])  # LIMIT TO 10 RECENT YEARS
    available_years = sorted(list(years_qs))  # sorted ascending

    year_counts = {
        year: Registration.objects.filter(date_of_establishment__year=year).count()
        for year in available_years
    }

    # Breakdown of companies by nature and year for comparison chart
    comparison_data = {}
    for year in available_years:
        year_data = Registration.objects.filter(date_of_establishment__year=year).values('nature').annotate(
            count=Count('id'))
        comparison_data[year] = {item['nature']: item['count'] for item in year_data}

    context = {
        'total_companies': total_companies,
        'total_individuals': total_individuals,

        # Chart labels and data
        'company_nature_labels': mark_safe(json.dumps([entry['nature'] for entry in company_nature])),
        'company_nature_data': mark_safe(json.dumps([entry['count'] for entry in company_nature])),

        'business_model_labels': mark_safe(json.dumps([entry['business_model'] for entry in business_model])),
        'business_model_data': mark_safe(json.dumps([entry['count'] for entry in business_model])),

        'stage_labels': mark_safe(json.dumps([entry['stage'] for entry in stage])),
        'stage_data': mark_safe(json.dumps([entry['count'] for entry in stage])),

        'year_labels': mark_safe(json.dumps(list(year_counts.keys()))),
        'year_data': mark_safe(json.dumps(list(year_counts.values()))),

        # Monthly comparison
        'month_labels': mark_safe(json.dumps(month_labels)),
        'all_years_data': mark_safe(json.dumps(all_years_data)),
        'available_years': mark_safe(json.dumps(list(available_years))),

        'available_years': available_years,
        'comparison_data': mark_safe(json.dumps(comparison_data)),

    }

    return render(request, 'dashboard.html', context)


'''
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
'''


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
            return JsonResponse({'status': 'error',
                                 'message': 'Password must be at least 8 characters long and include a capital letter, number, and symbol.'})

        # Encrypt the password
        encrypted_password = make_password(new_password)

        try:
            SignupUser.objects.filter(id=myId).update(password=encrypted_password)
            title = "Password Change"
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


# let's start displaying notifications
def notifications(request):
    myId = request.session.get('id')
    notif = Notification.objects.filter(user_id=myId, is_read=False)

    notif = Notification.objects.filter(user_id=myId, is_read=False)

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
    return render(request, 'viewNotification.html',data)

def markAsRead(request, pk):
    notification = get_object_or_404(Notification, pk=pk)
    notification.is_read = True
    notification.save()
    return redirect('notifications')  # or wherever you want to redirect

def viewMynotifications(request, pk):
    notification = get_object_or_404(Notification, pk=pk)

    # Optional: mark as read automatically on view
    if not notification.is_read:
        notification.is_read = True
        notification.save()

    return render(request, 'view_notification.html', {
        'notification': notification
    })
