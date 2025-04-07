from django.db import models

class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)
    nationality = models.CharField(max_length=100)
    class Meta:
        db_table = 'country'

    def __str__(self):
        return f"{self.name} ({self.nationality})"




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