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
    path('authlogoutSys/', views.authlogoutSys, name='authlogoutSys'),
    path('Adminprofile/', views.Adminprofile, name='Adminprofile'),
    path('editProfile/', views.profileChange, name='editProfileSys'),
    path('saveEditProfile/', views.saveEditProfile, name='saveEditProfileSys'),
    path('changeMyPassword/', views.resetPassword, name='changeMyPasswordSys'),
    path('saveChangeMyPassword/', views.saveChangeMyPassword, name='saveChangeMyPasswordSys'),
    path('notifications/', views.notifications, name='Sys_notifications'),
    path('markAsRead/<int:pk>/', views.markAsRead, name='markAsReadSys'),
    path('viewMynotifications/<int:pk>/', views.viewMynotifications, name='viewMynotificationsSys'),

]
