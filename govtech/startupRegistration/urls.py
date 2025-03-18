from django.contrib import admin
from django.urls import include, path
from django.urls import path
from .views import multi_step_registration, registration_complete
from django.urls import path
from .import views


from django.urls import path
from .views import dashboard

urlpatterns = [
    # path("", views.home, name="home"),
    path('register/', multi_step_registration, name='multi_step'),
    path('step/<int:step>/', multi_step_registration, name='multi_step'),
    path('completed/', registration_complete, name='registration_complete'),
    #path('dashboard/', dashboard, name='dashboard'),
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