from django.db import models

# Create your models here.


# models.py
from django.db import models

class Registration(models.Model):
    # Step 1: Basic Company Information
    startup_name = models.CharField(max_length=255)
    business_registration_number = models.CharField(max_length=100, blank=True, null=True)
    date_of_establishment = models.DateField()
    company_logo = models.ImageField(upload_to='logos/', blank=True, null=True)

    # Step 2: Contact Details
    official_email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    website = models.URLField(blank=True, null=True)
    physical_address = models.TextField()
    city_region = models.CharField(max_length=100)

    # Step 3: Founder & Team Information
    founder_name = models.CharField(max_length=255)
    founder_id = models.CharField(max_length=100)
    founder_contact = models.CharField(max_length=20)
    employees = models.IntegerField()

    # Step 4: Business Details
    startup_description = models.TextField()
    sector = models.CharField(max_length=100)
    business_model = models.CharField(max_length=50, choices=[('B2B', 'B2B'), ('B2C', 'B2C'), ('SaaS', 'SaaS'), ('Marketplace', 'Marketplace')])
    stage = models.CharField(max_length=50, choices=[('Idea', 'Idea'), ('MVP', 'MVP'), ('Early-stage', 'Early-stage'), ('Growth', 'Growth'), ('Scaling', 'Scaling')])
    revenue_model = models.TextField()

    # Step 5: Technology Stack & Innovation
    core_technologies = models.TextField()
    unique_value_proposition = models.TextField()
    ip_ownership = models.TextField(blank=True, null=True)

    # Step 6: Funding & Investment
    funding_status = models.CharField(max_length=255)
    key_investors = models.TextField(blank=True, null=True)

    # Step 7: Compliance & Legal Information
    business_certificate = models.FileField(upload_to='certificates/')
    tax_identification_number = models.CharField(max_length=100)
    licenses = models.TextField(blank=True, null=True)
    gdpr_compliance = models.BooleanField(default=False)

    # Step 8: Government Support & Expectations
    government_support_needed = models.TextField()
    challenges_faced = models.TextField()

    # Step 9: Declaration & Consent
    agree_terms = models.BooleanField(default=False)
    consent_data_usage = models.BooleanField(default=False)
    signature = models.TextField()

    def __str__(self):
        return self.startup_name
