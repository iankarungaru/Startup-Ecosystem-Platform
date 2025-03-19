from django.shortcuts import render,redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from validate_email_address import validate_email

# Create your views here.
def landing(request):
    return render(request, 'landing.html')

def register_view(request):
    if request.method == 'POST':
        # Get the data from the form
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        nationality = request.POST.get('nationality')
        county = request.POST.get('county')
        subcounty = request.POST.get('subcounty')
        gender = request.POST.get('gender')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        # Validate the email
        if validate_email(email):
            # Create a verification link (this is just a placeholder for now)
            verification_link = 'http://your-domain.com/verify/'  # Replace this later with the real link
            
            # Send the verification email
            send_mail(
                'Email Verification',
                f'Hi there,Welcome to Startup Kenya!Click the link to verify your email: {verification_link}',
                settings.DEFAULT_FROM_EMAIL,  # Sender email (defined in settings.py)
                [email],  # Recipient email
                fail_silently=False,
            )
            
            # Display a success message to the user
            messages.success(request, 'A verification email has been sent to your email address.')
            return redirect('login')  # Redirect the user to the login page or any other page
        
        else:
            # If email validation fails, show an error message
            messages.error(request, 'Please enter a valid email address.')
    
    # If the request method is GET, render the registration form
    return render(request, 'register.html')

# View for login page
def login_view(request):
    return render(request, 'login.html')

def authlogin(request): 
    return print("Hekoooo")
