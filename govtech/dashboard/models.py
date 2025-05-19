from django.db import models

# Create your models here.

# models.py
from django.db import models
from landingPage.models import SignupUser


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
    business_model = models.CharField(max_length=50, choices=[('B2B', 'B2B'), ('B2C', 'B2C'), ('SaaS', 'SaaS'),
                                                              ('Marketplace', 'Marketplace')])
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

class Notification(models.Model):
    user = models.ForeignKey(SignupUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)  # ← Move it inside the class!

    class Meta:
        # db_table = 'notifications'
        ordering = ['-created_at']

    def short_message(self):
        return (self.message[:50] + '...') if len(self.message) > 50 else self.message

    def __str__(self):
        return f"To: {self.user.id} | {self.title}"
