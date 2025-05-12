import re

from landingPage.models import Subcounty, County, Country, gender, SignupUser
from dashboard.models import Notification
from django.db import IntegrityError



def getSubcountyName(subcountyId):
    subcountyInfo = Subcounty.objects.get(id=subcountyId)
    subcountyName = subcountyInfo.name
    return subcountyName


def getCountyName(countyId):
    countyInfo = County.objects.get(id=countyId)
    countyName = countyInfo.name
    return countyName


def getGenderName(genderId):
    genderInfo = gender.objects.get(id=genderId)
    genderName = genderInfo.name
    return genderName


def getnationalityName(countryId):
    nationalityInfo = Country.objects.get(id=countryId)
    nationalityName = nationalityInfo.nationality
    return nationalityName


def getCountryName(countryId):
    countryInfo = Country.objects.get(id=countryId)
    countryName = countryInfo.name
    return countryName


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


