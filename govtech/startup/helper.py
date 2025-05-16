import re
import random
import string

from landingPage.models import Subcounty, County, Country, gender, SignupUser
from django.db import IntegrityError



def getSubcountyName(subcountyId):
    subcountyInfo = Subcounty.objects.get(id=subcountyId)
    subcountyName = subcountyInfo.name

    try:
        return subcountyName
    except Subcounty.DoesNotExist:
        return None

def getCountyName(countyId):
    countyInfo = County.objects.get(id=countyId)
    countyName = countyInfo.name
    try:
        return countyName
    except County.DoesNotExist:
        return None


def getGenderName(genderId):
    if not genderId:
        return None

    genderInfo = gender.objects.get(id=genderId)
    genderName = genderInfo.name

    try:
        return genderName
    except gender.DoesNotExist:
        return None


def getnationalityName(countryId):
    nationalityInfo = Country.objects.get(id=countryId)
    nationalityName = nationalityInfo.nationality
    try:
        return nationalityName
    except Country.DoesNotExist:
        return None


def getCountryName(countryId):
    countryInfo = Country.objects.get(id=countryId)
    countryName = countryInfo.name
    try:
        return countryName
    except Country.DoesNotExist:
        return None


def is_strong_password(password):
    # At least 8 characters, one uppercase letter, one number, and one symbol
    return (
            len(password) >= 8 and
            re.search(r'[A-Z]', password) and
            re.search(r'[a-z]', password) and
            re.search(r'\d', password) and
            re.search(r'[^A-Za-z0-9]', password)
    )


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def notification_insert(title, message, user_id, myModel):
    try:
        notif = myModel.objects.create(
            title=title,
            message=message,
            user_id=user_id,
            is_read = False,
        )
        notif.save()
        return {'status': 'success', 'id': notif.id}
    except IntegrityError as e:
        return {'status': 'error', 'message': f'Database error: {str(e)}'}
    except Exception as e:
        return {'status': 'error', 'message': f'Unexpected error: {str(e)}'}


def getAccountNames(id):
    try:
        user = SignupUser.objects.get(id=id)
        firstName = user.fName
        lastName = user.lName
        fullName = firstName + ' ' + lastName

        return fullName
    except IntegrityError as e:
        return {'status': 'error', 'message': f'Database error: {str(e)}'}
    except Exception as e:
        return {'status': 'error', 'message': f'Unexpected error: {str(e)}'}

def generate_strong_password(length=12):
    if length < 8:
        raise ValueError("Password length must be at least 8 characters")

    # Character sets
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    symbols = string.punctuation

    # Ensure the password contains at least one of each required character type
    password = [
        random.choice(lowercase),
        random.choice(uppercase),
        random.choice(digits),
        random.choice(symbols),
    ]

    # Fill the rest of the password length with random choices from all characters
    all_chars = lowercase + uppercase + digits + symbols
    password += random.choices(all_chars, k=length - 4)

    # Shuffle the list to make the order random
    random.shuffle(password)

    return ''.join(password)
