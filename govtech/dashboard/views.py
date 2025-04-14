from django.shortcuts import render, HttpResponse
import json
from datetime import datetime
from .models import Registration
from django.http import HttpResponse
from django.urls import reverse
from datetime import datetime
from .forms import (
    Step1Form, Step2Form, IndividualForm
)
from django.contrib.auth import logout
from django.http import JsonResponse
from landingPage.models import SignupUser
from startup.helper import *


def dashboard_data(request):
    return render(request, "dashboard.html")


def index(request):
    return render(request,"index.html")


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

    return render(request, "register/completed.html")



from django.shortcuts import render, redirect
from .forms import IndividualForm

def individual_reg(request):
    if request.method == 'POST':
        form = IndividualForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "register/completed.html")  # Adjust URL as needed
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
    }

    return render(request, 'myprofile.html', data)