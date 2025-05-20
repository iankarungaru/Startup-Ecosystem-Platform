from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings

def faq_view(request):
    return render(request, 'faq.html')

def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        send_mail(
            subject=f"DevLink Contact from {name}",
            message=message,
            from_email=email,
            recipient_list=[settings.DEFAULT_FROM_EMAIL],
        )

        return render(request, 'contact.html', {'success': True})
    return render(request, 'contact.html')