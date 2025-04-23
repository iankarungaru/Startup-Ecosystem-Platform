from landingPage.models import Subcounty, County ,Country, gender
import re
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