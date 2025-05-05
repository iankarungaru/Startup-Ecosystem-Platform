from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='sysadmin'),
    path('authorize_login/', views.authorize_login, name='authorize_login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('forgetPasswordSysAdmin/', views.forgetPasswordSysAdmin, name='forgetPasswordSysAdmin'),
    path('verificationLinkSys/', views.verificationLinkSys, name='verificationLinkSys'),
    path('otpVerificationSys/', views.otpVerificationSys, name='otpVerificationSys'),
    path('verifyOTPSys/', views.verifyOTPSys, name='verifyOTPSys'),
    path('ChangePasswordSys/', views.ChangePasswordSys, name='ChangePasswordSys'),
    path('saveForgetMyPasswordSys/', views.saveForgetMyPasswordSys, name='saveForgetMyPasswordSys'),


]
