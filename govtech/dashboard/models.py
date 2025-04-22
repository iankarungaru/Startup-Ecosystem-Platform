from django.db import models

# Create your models here.


# models.py
from django.db import models

class Registration(models.Model):
    # Step 1: Basic Company Information
    company_name = models.CharField(max_length=255)
    stage = models.CharField(max_length=50, choices=[
        ('Idea', 'Idea'),
        ('MVP', 'MVP'),
        ('Early-stage', 'Early-stage'),
        ('Growth', 'Growth'),
        ('Scaling', 'Scaling')
        ], default='Idea')
    official_email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    registration_number = models.CharField(max_length=255, default='CPR/201x/xxxxx')
    contact_person = models.CharField(max_length=255, default='John Doe')
    date_of_establishment = models.DateField()
    physical_address = models.TextField()
    
    # Step 2: Business Details
    tax_identification_number = models.CharField(max_length=100)
    employees = models.IntegerField()
    company_description = models.TextField()
    nature = models.CharField(max_length=50, choices=[
        ('Software Development', 'Software Development'),
        ('Web Services', 'Web Services'),
        ('Mobile Apps', 'Mobile Apps'),
        ('Desktop Apps', 'Desktop Apps'),
        ('IoT Apps', 'IoT Apps')
        ], default='Software Development')
    specialization = models.CharField(max_length=255, default='Web Development')
    sector = models.CharField(max_length=100)
    business_model = models.CharField(max_length=50, choices=[('B2B', 'B2B'), ('B2C', 'B2C'), ('SaaS', 'SaaS'), ('Marketplace', 'Marketplace')])
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.company_name
    
from django.db import models

class IndividualDev(models.Model):
    first_name = models.CharField(max_length=255)
    second_name = models.CharField(max_length=255)
    id_number = models.CharField(max_length=20)
    website = models.URLField(blank=True, null=True)
    mail = models.EmailField()
    contact = models.CharField(max_length=20)
    industry = models.CharField(max_length=100)
    address = models.TextField()
    nature = models.CharField(max_length=50, choices=[
        ('Software Development', 'Software Development'),
        ('Web Services', 'Web Services'),
        ('Mobile Apps', 'Mobile Apps'),
        ('Desktop Apps', 'Desktop Apps'),
        ('IoT Apps', 'IoT Apps')
        ], default='Software Development')
    description = models.TextField()

    def __str__(self):
        return f"{self.first_name} {self.second_name}"


'''from django.db import models

class DashboardData(models.Model):
    STARTUP_STAGE_CHOICES = [
        ('idea', 'Idea'),
        ('prototype', 'Prototype'),
        ('launch', 'Launch'),
        ('growth', 'Growth'),
        ('scaling', 'Scaling'),
    ]

    BUSINESS_MODEL_CHOICES = [
        ('b2b', 'B2B'),
        ('b2c', 'B2C'),
        ('marketplace', 'Marketplace'),
        ('saas', 'SaaS'),
        ('other', 'Other'),
    ]

    FUNDING_STATUS_CHOICES = [
        ('bootstrapped', 'Bootstrapped'),
        ('pre_seed', 'Pre-Seed'),
        ('seed', 'Seed'),
        ('series_a', 'Series A'),
        ('funded', 'Funded'),
    ]

    startup_name = models.CharField(max_length=255)
    official_email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    physical_address = models.CharField(max_length=255)
    website = models.URLField(blank=True, null=True)
    tax_identification_number = models.CharField(max_length=50)
    sector = models.CharField(max_length=100)
    business_model = models.CharField(max_length=50, choices=BUSINESS_MODEL_CHOICES)
    stage = models.CharField(max_length=50, choices=STARTUP_STAGE_CHOICES)
    funding_status = models.CharField(max_length=50, choices=FUNDING_STATUS_CHOICES)
    employees = models.PositiveIntegerField()
    date_of_establishment = models.DateField()
    startup_description = models.TextField()

    def __str__(self):
        return self.startup_name
'''