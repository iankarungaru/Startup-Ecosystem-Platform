# forms.py
from django import forms

class Step1Form(forms.Form):
    startup_name = forms.CharField(max_length=255, required=True)
    business_registration_number = forms.CharField(max_length=100, required=False)
    date_of_establishment = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))
    company_logo = forms.ImageField(required=False)

class Step2Form(forms.Form):
    official_email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=20, required=True)
    website = forms.URLField(required=False)
    physical_address = forms.CharField(widget=forms.Textarea, required=True)
    city_region = forms.CharField(max_length=100, required=True)

class Step3Form(forms.Form):
    founder_name = forms.CharField(max_length=255, required=True)
    founder_id = forms.CharField(max_length=100, required=True)
    founder_contact = forms.CharField(max_length=20, required=True)
    employees = forms.IntegerField(min_value=1, required=True)

class Step4Form(forms.Form):
    startup_description = forms.CharField(widget=forms.Textarea, required=True)
    sector = forms.CharField(max_length=100, required=True)
    business_model = forms.ChoiceField(choices=[('B2B', 'B2B'), ('B2C', 'B2C'), ('SaaS', 'SaaS'), ('Marketplace', 'Marketplace')], required=True)
    stage = forms.ChoiceField(choices=[('Idea', 'Idea'), ('MVP', 'MVP'), ('Early-stage', 'Early-stage'), ('Growth', 'Growth'), ('Scaling', 'Scaling')], required=True)
    revenue_model = forms.CharField(widget=forms.Textarea, required=True)

class Step5Form(forms.Form):
    core_technologies = forms.CharField(widget=forms.Textarea, required=True)
    unique_value_proposition = forms.CharField(widget=forms.Textarea, required=True)
    ip_ownership = forms.CharField(widget=forms.Textarea, required=False)

class Step6Form(forms.Form):
    funding_status = forms.CharField(max_length=255, required=True)
    key_investors = forms.CharField(widget=forms.Textarea, required=False)

class Step7Form(forms.Form):
    business_certificate = forms.FileField(required=True)
    tax_identification_number = forms.CharField(max_length=100, required=True)
    licenses = forms.CharField(widget=forms.Textarea, required=False)
    gdpr_compliance = forms.BooleanField(required=False)

class Step8Form(forms.Form):
    government_support_needed = forms.CharField(widget=forms.Textarea, required=True)
    challenges_faced = forms.CharField(widget=forms.Textarea, required=True)

class Step9Form(forms.Form):
    agree_terms = forms.BooleanField(required=True)
    consent_data_usage = forms.BooleanField(required=True)
    signature = forms.CharField(widget=forms.Textarea, required=True)