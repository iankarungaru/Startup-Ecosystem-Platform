from django.shortcuts import redirect
import re

EXEMPT_URLS = [
    r'^$',  # homepage
    r'^register/?$',
    r'^login/?$',              # public login
    r'^authlogin/.*$',
    r'^get-subcounties/.*$',
    r'^signup/.*$',
    r'^forgetPassword/.*$',
    r'^verificationLink/.*$',
    r'^otpVerification/.*$',
    r'^verifyOTP/.*$',
    r'^ChangePassword/.*$',
    r'^saveForgetMyPassword/.*$',
    r'^force-password-change(/.*)?$',
    r'^sysadmin/?$',           # sysadmin login
    r'^sysadmin/login/?$',
    r'^sysadmin/authorize_login/.*$',
    r'^sysadmin/forgetPasswordSysAdmin/.*$',
    r'^sysadmin/verificationLinkSys/.*$',
    r'^sysadmin/otpVerificationSys/.*$',
    r'^sysadmin/verifyOTPSys/.*$',
    r'^sysadmin/ChangePasswordSys/.*$',
    r'^sysadmin/saveForgetMyPasswordSys/.*$',
]

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.exempt_urls = [re.compile(expr) for expr in EXEMPT_URLS]

    def __call__(self, request):
        path = request.path_info.lstrip('/')

        if any(pattern.match(path) for pattern in self.exempt_urls):
            # Flush session (clears everything including auth session)
            request.session.flush()
            return self.get_response(request)

        # If not authenticated, redirect accordingly
        if not request.user.is_authenticated:
            if path.startswith('sysadmin/'):
                return redirect('/sysadmin/')
            else:
                return redirect('/login/')

        return self.get_response(request)
