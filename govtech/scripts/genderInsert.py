import os
import sys
import django

# Add the root directory of the project to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Set DJANGO_SETTINGS_MODULE to point to the correct path
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "startup.settings")

# Setup Django
django.setup()


# Now you can import models from landingPage
from landingPage.models import gender  # Adjust the model name if needed

genders = ["Male", "Female", "Other"]

for g in genders:
    _, created = gender.objects.get_or_create(name=g)
    if created:
        print(f"✅ Inserted gender: {g}")
    else:
        print(f"⚠️ Gender already exists: {g}")
