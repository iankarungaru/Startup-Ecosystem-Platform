from django.db import models
from django.utils import timezone

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






# # landingPage/models.py
# from django.db import models
# from django.contrib.auth.models import AbstractUser, UserManager

# class CustomUserManager(UserManager):
#     def create_user(self, email, password=None, **extra_fields):
#         if not email:
#             raise ValueError('The Email field must be set')
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         return self.create_user(email, password, **extra_fields)

# class CustomUser(AbstractUser):
#     username = None
#     email = models.EmailField(unique=True, max_length=255)
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     phone = models.CharField(max_length=15, blank=True, null=True)
#     nationality = models.CharField(max_length=100)
#     county = models.CharField(max_length=100)
#     subcounty = models.CharField(max_length=100)
#     gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')])

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['first_name', 'last_name', 'nationality', 'county', 'subcounty', 'gender']

#     objects = CustomUserManager()

#     def __str__(self):
#         return self.email