from django.contrib import admin
from django.urls import path
from .views import dashboard, multi_step_registration, registration_complete, individual_reg
from django.conf import settings
from django.conf.urls.static import static

# No app_name = 'dashboard' here, good.

urlpatterns = [
    path('register/step/<int:step>/', multi_step_registration, name='multi_step'),
    path('completed/', registration_complete, name='registration_complete'),
    path('individual/', individual_reg, name='individual_reg'),
    path('dashboard/', dashboard, name='dashboard'),
]

# Media files
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
