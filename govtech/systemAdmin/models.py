from django.db import models
from django.utils import timezone
from datetime import timedelta

class InternalUser(models.Model):
    fName = models.CharField(max_length=255)
    lName = models.CharField(max_length=255)
    idNo = models.PositiveIntegerField(unique=True)
    email = models.EmailField(max_length=255, unique=True)
    phone = models.CharField(max_length=20)
    nationality = models.PositiveIntegerField()
    county = models.PositiveIntegerField()
    subcounty = models.PositiveIntegerField()
    gender = models.PositiveSmallIntegerField(null=True, blank=True)
    password = models.TextField()
    profile_picture = models.CharField(max_length=255, blank=True, null=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    isLogin = models.BooleanField(default=False)
    logtime = models.DateTimeField(auto_now_add=True)
    isactive = models.BooleanField(default=True)
    dateCreated = models.DateTimeField(auto_now_add=True)
    dateUpdated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'internalusers'

    def __str__(self):
        return f"{self.fName} {self.lName}"

class AttemptLogin(models.Model):
    email = models.EmailField()
    ip_address = models.GenericIPAddressField()
    attempts = models.IntegerField(default=0)
    last_attempt = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'attempt_login'

    def is_locked_out(self):
        # You can lockout after 5 attempts within 10 minutes, for example
        return self.attempts >= 5 and timezone.now() - self.last_attempt < timedelta(minutes=10)

    def reset_if_expired(self):
        if timezone.now() - self.last_attempt > timedelta(minutes=10):
            self.attempts = 0
            self.save()

class PasswordResetToken(models.Model):
    user = models.ForeignKey('InternalUser', on_delete=models.CASCADE)
    token = models.CharField(max_length=8)  # OTPs are 8-char, alphanumeric
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        # Valid for 10 minutes
        return timezone.now() < self.created_at + timedelta(minutes=10)

    class Meta:
        db_table = 'password_reset_token'

    def __str__(self):
        return f'Token for {self.user.email}'