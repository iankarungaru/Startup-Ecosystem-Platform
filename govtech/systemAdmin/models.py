from django.db import models

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
