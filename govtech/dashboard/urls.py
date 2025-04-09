from django.contrib import admin
from django.urls import include, path
from django.urls import path
from .views import multi_step_registration, registration_complete, individual_reg, dashboard_data, index, authlogout # DashboardData
from django.urls import path


#app_name = 'startupRegistration'  # ✅ Set the app name to 'dashboard'


urlpatterns = [
    # path("", views.home, name="home"),
    path('SoftwareFirm/', multi_step_registration, name='multi_step'),
    path('step/<int:step>/', multi_step_registration, name='multi_step'),
    path('completed/', registration_complete, name='registration_complete'),
    path('individual/', individual_reg, name='individual_reg'),
    path('',  dashboard_data, name='dashboard'),
    path("index/", index, name="index"),
    path("authlogout/", authlogout, name="authlogout"),
]


from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)













'''
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    path('newsletter/', include('newsletter.urls')),
]
'''