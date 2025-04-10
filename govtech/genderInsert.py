# landingPage/scripts/insert_genders.py

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yourproject.settings')  # 🔁 Replace with your project name
django.setup()

from landingPage.models import gender  # 👈 Adjust if your model is in a different location

genders = ["Male", "Female", "Other"]

for g in genders:
    _, created = gender.objects.get_or_create(name=g)
    if created:
        print(f"✅ Inserted gender: {g}")
    else:
        print(f"⚠️ Gender already exists: {g}")
