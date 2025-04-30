from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='sysadmin'),
    path('authorize_login/', views.authorize_login, name='authorize_login'),
    path('dashboard/', views.dashboard, name='dashboard'),

]
