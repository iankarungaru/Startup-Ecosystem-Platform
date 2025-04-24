from django.db import models
from django.utils import timezone
from datetime import timedelta

class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)
    nationality = models.CharField(max_length=100)
    
    class Meta:
        db_table = 'country'

    def __str__(self):
        return f"{self.name} ({self.nationality})"

class County(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Ensuring county names are unique
    class Meta:
        db_table = 'county'
    def __str__(self):
        return self.name

class Subcounty(models.Model):
    name = models.CharField(max_length=100)  
    county = models.ForeignKey(County, on_delete=models.CASCADE, related_name='subcounties')  # Foreign key to County

    class Meta:
        db_table = 'subcounty'  # The name of the table in the database

    def __str__(self):
        return self.name

class gender(models.Model):
    name = models.CharField(max_length=100, unique=True)
    class Meta:
        db_table = 'gender'

    def __str__(self):
        return self.name
    
class SignupUser(models.Model):
    fName = models.CharField(max_length=255)
    lName = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    phone = models.CharField(max_length=255)
    nationality = models.IntegerField()
    county = models.IntegerField()
    subcounty = models.IntegerField()
    gender = models.IntegerField(null=True, blank=True)  # Nullable in DB
    password = models.TextField()
    isLogin = models.IntegerField(default=0)
    logtime = models.DateTimeField(auto_now_add=True)
    isactive = models.IntegerField(default=0)
    dateCreated = models.DateTimeField(auto_now_add=True) 
    dateUpdated = models.DateTimeField(auto_now=True) 

    class Meta:
        db_table = 'externalusers'  # Change this to your actual DB table name

    def __str__(self):
        return self.email


class LoginAttempt(models.Model):
    email = models.EmailField()
    ip_address = models.GenericIPAddressField()
    attempts = models.IntegerField(default=0)
    last_attempt = models.DateTimeField(auto_now=True)

    def is_locked_out(self):
        # You can lockout after 5 attempts within 10 minutes, for example
        return self.attempts >= 5 and timezone.now() - self.last_attempt < timedelta(minutes=10)

    def reset_if_expired(self):
        if timezone.now() - self.last_attempt > timedelta(minutes=10):
            self.attempts = 0
            self.save()