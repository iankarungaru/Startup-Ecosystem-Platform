import os
import django
import sys
import socket
from django.contrib.auth.hashers import make_password

# Setup Django project
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "startup.settings")
django.setup()

from systemAdmin.models import InternalUser

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception as e:
        return "127.0.0.1"  # fallback to localhost

from django.db import connections

def create_admin_user():
    try:
        # Explicitly query against sysadmin DB
        if InternalUser.objects.using('sysadmin').filter(email="noemail@moict.go.ke").exists():
            print("ℹ️  Admin user already exists.")
            return 0

        password = "Pass987@moict!*"
        encrypted_password = make_password(password)

        InternalUser.objects.using('sysadmin').create(
            fName="System",
            lName="Administrator",
            idNo="22889036",
            email="noemail@moict.go.ke",
            phone="0798765432",
            nationality="73",
            county="30",
            subcounty="199",
            gender="3",
            password=encrypted_password,
            ip_address=get_local_ip(),
            isactive="0",
            pswdchange="0"
        )
        print("✅ Admin user created successfully.")
        return 0
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")
        return 1


# Only run if script is called directly
if __name__ == "__main__":
    exit_code = create_admin_user()
    sys.exit(exit_code)
