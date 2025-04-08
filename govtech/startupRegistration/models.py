from django.db import models

# Create your models here.


# models.py
from django.db import models

class Registration(models.Model):
    # Step 1: Basic Company Information
    startup_name = models.CharField(max_length=255)
    stage = models.CharField(max_length=50, choices=[('Idea', 'Idea'), ('MVP', 'MVP'), ('Early-stage', 'Early-stage'), ('Growth', 'Growth'), ('Scaling', 'Scaling')])
    official_email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    date_of_establishment = models.DateField()
    physical_address = models.TextField()
    
    # Step 2: Business Details
    tax_identification_number = models.CharField(max_length=100)
    employees = models.IntegerField()
    startup_description = models.TextField()
    sector = models.CharField(max_length=100)
    business_model = models.CharField(max_length=50, choices=[('B2B', 'B2B'), ('B2C', 'B2C'), ('SaaS', 'SaaS'), ('Marketplace', 'Marketplace')])
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.startup_name
