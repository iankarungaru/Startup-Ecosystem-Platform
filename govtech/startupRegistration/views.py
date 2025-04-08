from django.shortcuts import render, HttpResponse
import json
from datetime import datetime
# Create your views here

# views.py

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from datetime import datetime
from .forms import (
    Step1Form, Step2Form, IndividualForm
)

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



# views.py for dashboard

from django.shortcuts import render
from django.db.models import Count, Avg
from .models import Registration

def dashboard(request):
    # Get total registrations
    total_registrations = Registration.objects.count()

    # Get average number of employees
    avg_employees = Registration.objects.aggregate(Avg('employees'))['employees__avg'] or 0
    avg_employees = round(avg_employees, 2)

    # Get the most common industry
    common_industry = Registration.objects.values('sector').annotate(count=Count('sector')).order_by('-count').first()
    common_industry = common_industry['sector'] if common_industry else 'N/A'

    # Get all registrations for the table
    registrations = Registration.objects.all()

    # Business Model Distribution
    business_model_data = Registration.objects.values('business_model').annotate(count=Count('business_model'))
    business_model_labels = [item['business_model'] for item in business_model_data]
    business_model_counts = [item['count'] for item in business_model_data]

    # Startup Stage Distribution
    startup_stage_data = Registration.objects.values('stage').annotate(count=Count('stage'))
    startup_stage_labels = [item['stage'] for item in startup_stage_data]
    startup_stage_counts = [item['count'] for item in startup_stage_data]

    # Funding Status Distribution
    funding_status_data = Registration.objects.values('funding_status').annotate(count=Count('funding_status'))
    funding_labels = [item['funding_status'] for item in funding_status_data]
    funding_counts = [item['count'] for item in funding_status_data]

    context = {
        'total_registrations': total_registrations,
        'avg_employees': avg_employees,
        'common_industry': common_industry,
        'registrations': registrations,
        'business_model_labels': business_model_labels,
        'business_model_counts': business_model_counts,
        'startup_stage_labels': startup_stage_labels,
        'startup_stage_counts': startup_stage_counts,
        'funding_labels': funding_labels,
        'funding_counts': funding_counts,
    }
    return render(request, 'dashboard.html', context)




