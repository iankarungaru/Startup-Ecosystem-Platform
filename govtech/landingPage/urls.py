from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),  
    path('authlogin/', views.authlogin, name = 'authlogin'),
    path('get-subcounties/', views.get_subcounties, name='get_subcounties'),
    path('signup/', views.signup, name='signup'),
    path('forgetPassword/', views.forgetPassword, name='forgetPassword'),
    path('verificationLink/', views.verificationLink, name='verificationLink'),
    path('otpVerification/', views.otpVerification, name='otpVerification'),
    path('verifyOTP/', views.verifyOTP, name='verifyOTP'),
    path('ChangePassword/', views.ChangePassword, name='ChangePassword'),
    path('saveForgetMyPassword/', views.saveForgetMyPassword, name='saveForgetMyPassword'),
    path('force-password-change/<int:user_id>/', views.force_password_change, name='force_password_change'),


]
