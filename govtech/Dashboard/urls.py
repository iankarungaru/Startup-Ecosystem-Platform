from django.urls import path
from . import views
app_name = 'dashboard'  # ✅ Set the app name to 'dashboard'

urlpatterns = [
    # path("", views.home, name="home"),
    path("dashboard/",views.dashboard, name="dashboard"),
    path("index/",views.index, name="index"),
]
