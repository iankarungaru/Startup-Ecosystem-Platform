# govtech/startup/middleware/login_required_middleware.py

from django.shortcuts import redirect
from django.conf import settings
import re

EXEMPT_URLS = [
    r'^$',
    r'^register/?$',                   
    r'^login/?$',
    r'^authlogin/.*$',
    r'^get-subcounties/.*$',    
    r'^signup/.*$',
    r'^forgetPassword/.*$',
    r'^verificationLink/.*$',
]

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.exempt_urls = [re.compile(expr) for expr in EXEMPT_URLS]

    def __call__(self, request):
        path = request.path_info.lstrip('/')
        if not request.user.is_authenticated:
            if not any(pattern.match(path) for pattern in self.exempt_urls):
                return redirect('/login/')
        return self.get_response(request)
