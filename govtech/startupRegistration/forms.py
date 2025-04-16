# forms.py
from django import forms
#chriss adjustments
import re
from .models import Individual

class Step1Form(forms.Form):
    startup_name = forms.CharField(max_length=255, required=True)
    stage = forms.ChoiceField(choices=[('Sole Proprietorship', 'Sole Proprietorship'), ('Limited Liability Company (LLC)', 'Limited Liability Company (LLC)'), ('Limited Liability Partnership (LLP)', 'Limited Liability Partnership (LLP)')], required=True)
    official_email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=20, required=True)
    date_of_establishment = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))
    physical_address = forms.CharField(widget=forms.Textarea, required=True)
    

class Step2Form(forms.Form):
    tax_identification_number = forms.CharField(max_length=100, required=True)
    employees = forms.IntegerField(min_value=1, required=True)
    business_model = forms.ChoiceField(choices=[('B2B', 'B2B'), ('B2C', 'B2C'), ('SaaS', 'SaaS'), ('Marketplace', 'Marketplace')], required=True)
    startup_description = forms.CharField(widget=forms.Textarea, required=True)
    sector = forms.CharField(max_length=100, required=True)
    website = forms.URLField(required=False)

    # Chriss adjustments

class IndividualForm(forms.ModelForm):
    class Meta:
        model = Individual
        fields = '__all__'

    def clean_full_name(self):
        name = self.cleaned_data.get('full_name')
        if not re.match(r'^[A-Za-z ]+$', name):
            raise forms.ValidationError("Full Name must only contain letters and spaces.")
        return name

    def clean_id_number(self):
        id_num = self.cleaned_data.get('id_number')
        if not id_num.isdigit():
            raise forms.ValidationError("ID Number must only contain digits.")
        return id_num

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if not phone.isdigit():
            raise forms.ValidationError("Phone Number must only contain digits.")
        return phone
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        return email.lower()  # ensure emails stored in lower case