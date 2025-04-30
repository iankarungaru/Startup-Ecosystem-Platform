import subprocess
import os
import sys
import django
import importlib.util
import mysql.connector
from django.conf import settings

# Add the root directory of the project to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Set DJANGO_SETTINGS_MODULE and setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "startup.settings")
django.setup()


def is_package_installed(package_name):
    try:
        importlib.import_module(package_name)
        return True
    except ImportError:
        return False


def install_mysql_connector():
    if not is_package_installed('mysql.connector'):
        print("⚠️ mysql-connector-python not found. Installing it now...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "mysql-connector-python"])
        print("✅ mysql-connector-python installed.")


def check_and_create_database(db_config):
    print(f"🔍 Checking if '{db_config['NAME']}' database exists...")

    connection = mysql.connector.connect(
        host=db_config['HOST'],
        user=db_config['USER'],
        password=db_config['PASSWORD']
    )

    cursor = connection.cursor()
    cursor.execute("SHOW DATABASES LIKE %s", (db_config['NAME'],))
    result = cursor.fetchone()

    if result:
        print(f"✅ Database '{db_config['NAME']}' already exists.")
    else:
        cursor.execute(f"CREATE DATABASE {db_config['NAME']}")
        print(f"✅ Database '{db_config['NAME']}' created.")

    cursor.close()
    connection.close()


def install_dependencies():
    print("📦 Installing requirements.txt dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    print("✅ All packages installed.\n")


def run_migrations():
    print("🔄 Running migrations...")

    manage_py_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'manage.py'))

    subprocess.check_call([sys.executable, manage_py_path, "makemigrations"])

    print("📁 Migrating to 'default' DB...")
    subprocess.check_call([sys.executable, manage_py_path, "migrate", "--database=default"])

    print("📁 Migrating to 'sysadmin' DB...")
    subprocess.check_call([sys.executable, manage_py_path, "migrate", "--database=sysadmin"])

    print("✅ Migrations completed.\n")


def run_scripts():
    print("⚙️ Running custom data scripts...\n")
    scripts = ["county.py", "genderInsert.py", "load_countries.py"]
    for script in scripts:
        script_path = os.path.join(os.path.dirname(__file__), script)
        if os.path.exists(script_path):
            print(f"➡️ Running {script}...")
            subprocess.check_call([sys.executable, script_path])
        else:
            print(f"⚠️ Script not found: {script}")
    print("\n✅ All setup scripts executed.")


if __name__ == "__main__":
    install_mysql_connector()
    install_dependencies()

    # Check and create both databases
    check_and_create_database(settings.DATABASES['default'])
    check_and_create_database(settings.DATABASES['sysadmin'])

    run_migrations()
    run_scripts()

    print("🚀 Setup complete!")
