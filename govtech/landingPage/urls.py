from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),  
    path('authlogin/', views.authlogin, name = 'authlogin'),
    path('get-subcounties/', views.get_subcounties, name='get_subcounties'),
    path('signup/', views.signup, name='signup'),
    

]
