import subprocess
import os
import django
import sys

# Prompt user to confirm if database 'startup' exists
confirmation = input("❓ Have you created a MySQL database named 'startup'? (yes/no): ").strip().lower()

if confirmation != "yes":
    print("⚠️ Please create a database named 'startup' before running this setup.")
    sys.exit(1)

# Add the root directory of the project to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Set DJANGO_SETTINGS_MODULE to point to the correct path
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "startup.settings")
django.setup()

def install_dependencies():
    print("📦 Installing dependencies...")
    subprocess.check_call(["pip", "install", "-r", "requirements.txt"])
    print("✅ Packages installed.\n")

def run_migrations():
    print("🔄 Running migrations...")
    
    # Set the correct path to manage.py by going up one level to the 'govtech' directory
    project_root = os.path.abspath(os.path.dirname(__file__))
    manage_py_path = os.path.join(os.path.dirname(project_root), "manage.py")

    # Run migrations
    subprocess.check_call(["python", manage_py_path, "makemigrations"])
    subprocess.check_call(["python", manage_py_path, "migrate"])
    print("✅ Migrations applied.\n")

def run_scripts():
    print("⚙️ Running custom setup scripts...\n")
    scripts = ["county.py", "genderInsert.py", "load_countries.py"]
    for script in scripts:
        print(f"➡️ Running {script}")
        subprocess.check_call(["python", script])
    print("\n✅ All setup scripts completed.")

if __name__ == "__main__":
    install_dependencies()  # Install dependencies first
    run_migrations()        # Apply migrations after installing dependencies
    run_scripts()           # Run custom setup scripts after migrations
    print("🚀 Setup complete!")
