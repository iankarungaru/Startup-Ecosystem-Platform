from landingPage.models import Subcounty, County ,Country, gender
def getSubcountyName(subcountyId):
    subcountyInfo = Subcounty.objects.get(id=subcountyId)
    subcountyName = subcountyInfo.name
    return subcountyName

def getCountyName(countyId):
    countyInfo = County.objects.get(id=countyId)
    countyName = countyInfo.name
    return countyName

def getGenderName(genderId):
    genderInfo = County.objects.get(id=genderId)
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