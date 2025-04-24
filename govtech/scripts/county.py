import os
import django
import sys

# Add the root directory of the project to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Set DJANGO_SETTINGS_MODULE to point to the correct path
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "startup.settings")

# Setup Django
django.setup()

# Now you can import models from landingPage
from landingPage.models import County, Subcounty


county_data = {
    "Baringo": ["Baringo North", "Baringo South", "Mogotio", "Eldama Ravine", "Tiaty"],
            "Bomet": ["Bomet Central", "Bomet East", "Chepalungu", "Sotik", "Konoin"],
            "Bungoma": ["Bungoma Central", "Bungoma East", "Bungoma South", "Bungoma North", "Mt. Elgon"],
            "Busia": ["Butula", "Funyula", "Nambale", "Samia", "Teso North", "Teso South"],
            "Elgeyo-Marakwet": ["Keiyo North", "Keiyo South", "Marakwet East", "Marakwet West"],
            "Embu": ["Embu East", "Embu North", "Embu West", "Mbeere North", "Mbeere South"],
            "Garissa": ["Balambala", "Dadaab", "Fafi", "Garissa Township", "Hulugho", "Ijara", "Lagdera"],
            "Homa Bay": ["Homa Bay Town", "Karachuonyo", "Mbita", "Ndhiwa", "Rachuonyo East", "Rachuonyo North", "Rachuonyo South"],
            "Isiolo": ["Garbatulla", "Isiolo", "Merti"],
            "Kajiado": ["Kajiado Central", "Kajiado East", "Kajiado North", "Kajiado South", "Kajiado West"],
            "Kakamega": ["Butere", "Khwisero", "Lugari", "Lurambi", "Mumias East", "Mumias West", "Navakholo", "Shinyalu"],
            "Kericho": ["Ainamoi", "Belgut", "Bureti", "Kipkelion East", "Kipkelion West", "Soin/Sigowet"],
            "Kiambu": ["Gatundu North", "Gatundu South", "Githunguri", "Juja", "Kabete", "Kiambaa", "Kiambu Town", "Kikuyu", "Lari", "Limuru", "Ruiru", "Thika Town"],
            "Kilifi": ["Ganze", "Kaloleni", "Kilifi North", "Kilifi South", "Magarini", "Malindi", "Rabai"],
            "Kirinyaga": ["Kirinyaga Central", "Kirinyaga East", "Kirinyaga West", "Mwea East", "Mwea West"],
            "Kisii": ["Bobasi", "Bomachoge Borabu", "Bomachoge Chache", "Kitutu Chache North", "Kitutu Chache South", "Nyaribari Chache", "Nyaribari Masaba", "South Mugirango"],
            "Kisumu": ["Kisumu Central", "Kisumu East", "Kisumu West", "Muhoroni", "Nyakach", "Nyando", "Seme"],
            "Kitui": ["Ikutha", "Katulani", "Kisasi", "Kitui Central", "Kitui East", "Kitui Rural", "Kitui South", "Kitui West", "Mutitu", "Mwingi Central", "Mwingi North", "Mwingi West"],
            "Kwale": ["Kinango", "Lunga Lunga", "Matuga", "Msambweni"],
            "Laikipia": ["Laikipia Central", "Laikipia East", "Laikipia North", "Laikipia West"],
            "Lamu": ["Lamu East", "Lamu West"],
            "Machakos": ["Kathiani", "Kangundo", "Machakos Town", "Masinga", "Matungulu", "Mavoko", "Mwala", "Yatta"],
            "Makueni": ["Kaiti", "Kilome", "Makueni", "Mbooni", "Mukaa", "Nzaui", "Wote"],
            "Mandera": ["Banissa", "Lafey", "Mandera Central", "Mandera East", "Mandera North", "Mandera South"],
            "Meru": ["Buuri", "Igembe Central", "Igembe North", "Igembe South", "Meru Central", "Meru North", "Meru South", "Tigania East", "Tigania West"],
            "Migori": ["Awendo", "Kuria East", "Kuria West", "Nyatike", "Rongo", "Suna East", "Suna West", "Uriri"],
            "Marsabit": ["Laisamis", "Moyale", "North Horr", "Saku"],
            "Mombasa": ["Changamwe", "Jomvu", "Kisauni", "Likoni", "Mvita", "Nyali"],
            "Murang'a": ["Gatanga", "Kahuro", "Kandara", "Kangema", "Kigumo", "Kiharu", "Maragua", "Mathioya"],
            "Nairobi": ["Dagoretti North", "Dagoretti South", "Embakasi Central", "Embakasi East", "Embakasi North", "Embakasi South", "Embakasi West", "Kamukunji", "Kasarani", "Kibra", "Lang'ata", "Makadara", "Mathare", "Roysambu", "Ruaraka", "Starehe", "Westlands"],
            "Nakuru": ["Bahati", "Gilgil", "Kuresoi North", "Kuresoi South", "Molo", "Naivasha", "Nakuru Town East", "Nakuru Town West", "Njoro", "Rongai", "Subukia"],
            "Nandi": ["Aldai", "Chesumei", "Emgwen", "Mosop", "Nandi Hills", "Tindiret"],
            "Narok": ["Narok East", "Narok North", "Narok South", "Narok West", "Trans Mara East", "Trans Mara West"],
            "Nyamira": ["Borabu", "Manga", "Masaba North", "Nyamira North", "Nyamira South"],
            "Nyandarua": ["Kinangop", "Kipipiri", "Ndaragwa", "Ol Kalou", "Ol Joro Orok"],
            "Nyeri": ["Kieni East", "Kieni West", "Mathira East", "Mathira West", "Mukurweini", "Nyeri Town", "Othaya", "Tetu"],
            "Samburu": ["Samburu Central", "Samburu East", "Samburu North"],
            "Siaya": ["Alego Usonga", "Bondo", "Gem", "Rarieda", "Ugenya", "Ugunja"],
            "Taita-Taveta": ["Mwatate", "Taveta", "Voi", "Wundanyi"],
            "Tana River": ["Bura", "Galole", "Garsen"],
            "Tharaka-Nithi": ["Chuka", "Igambang'ombe", "Maara", "Tharaka North", "Tharaka South"],
            "Trans Nzoia": ["Cherangany", "Endebess", "Kwanza", "Saboti", "Kiminini"],
            "Turkana": ["Loima", "Turkana Central", "Turkana East", "Turkana North", "Turkana South", "Turkana West"],
            "Uasin Gishu": ["Ainabkoi", "Kapseret", "Kesses", "Moiben", "Soy", "Turbo"],
            "Vihiga": ["Emuhaya", "Hamisi", "Luanda", "Sabatia", "Vihiga"],
            "Wajir": ["Bute", "Eldas", "Habasawein", "Tarbaj", "Wajir East", "Wajir North", "Wajir South", "Wajir West"],
            "West Pokot": ["Kacheliba", "Kapenguria", "Pokot South", "Sigor"]
    # Add other counties and subcounties here...
}

# Insert counties and subcounties
for county_name, subcounties in county_data.items():
    county = County.objects.create(name=county_name)
    for subcounty_name in subcounties:
        Subcounty.objects.create(name=subcounty_name, county=county)
