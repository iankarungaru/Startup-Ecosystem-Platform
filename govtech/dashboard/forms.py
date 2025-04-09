# forms.py
from django import forms

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

from django import forms
from .models import IndividualDev

class IndividualForm(forms.ModelForm):
    class Meta:
        model = IndividualDev
        fields = '__all__'  # or list them explicitly if needed

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'second_name': forms.TextInput(attrs={'class': 'form-control'}),
            'id_number': forms.TextInput(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'mail': forms.EmailInput(attrs={'class': 'form-control'}),
            'contact': forms.TextInput(attrs={'class': 'form-control'}),
            'industry': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
