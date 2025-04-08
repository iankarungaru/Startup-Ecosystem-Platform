from django.shortcuts import redirect
from django.urls import reverse

EXEMPT_PATHS = [
    '/',  # Landing page
    '/authlogin/',
    '/register/',
    '/logout/',
]

PROTECTED_PREFIXES = [
    '/dashboard/',
    '/account/',
]

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip if path is exempt
        if request.path in EXEMPT_PATHS:
            return self.get_response(request)

        # Check if it's under a protected path and user is not logged in
        if any(request.path.startswith(prefix) for prefix in PROTECTED_PREFIXES):
            if not request.user.is_authenticated:
                return redirect(reverse('login'))  # You can customize this URL

        return self.get_response(request)
