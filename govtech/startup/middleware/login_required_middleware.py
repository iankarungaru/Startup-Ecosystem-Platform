from django.shortcuts import redirect
import re

EXEMPT_URLS = [
    r'^$',
    r'^register/?$',
    r'^login/?$',  # General login page exemption
    r'^authlogin/.*$',
    r'^get-subcounties/.*$',
    r'^signup/.*$',
    r'^forgetPassword/.*$',
    r'^verificationLink/.*$',
    r'^otpVerification/.*$',
    r'^verifyOTP/.*$',
    r'^ChangePassword/.*$',
    r'^saveForgetMyPassword/.*$',


    # Exempt the sysadmin's homepage route (sysadmin section) and login
    r'^sysadmin/?$',  # Exempt sysadmin's login page and root route
    r'^sysadmin/login/?$',  # Exempt sysadmin's login page route
]

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.exempt_urls = [re.compile(expr) for expr in EXEMPT_URLS]

    def __call__(self, request):
        path = request.path_info.lstrip('/')
        # Check if the user is authenticated and the path is not exempted
        if not request.user.is_authenticated:
            if not any(pattern.match(path) for pattern in self.exempt_urls):
                # Redirect to the sysadmin login page or sysadmin homepage
                return redirect('/sysadmin/')  # Redirect to sysadmin section
        return self.get_response(request)
