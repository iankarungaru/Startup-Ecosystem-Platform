from django.urls import path
from .views import multi_step_registration, registration_complete, individual_reg, dashboard_data, index, authlogout, \
    Myprofile, profileChange, saveEditProfile, mySupport, resetPassword,saveChangeMyPassword  # DashboardData

urlpatterns = [
    # path("", views.home, name="home"),
    path('SoftwareFirm/', multi_step_registration, name='multi_step'),
    path('step/<int:step>/', multi_step_registration, name='multi_step'),
    path('completed/', registration_complete, name='registration_complete'),
    path('individual/', individual_reg, name='individual_reg'),
    path('', dashboard_data, name='dashboard'),
    path("index/", index, name="index"),
    path("authlogout/", authlogout, name="authlogout"),
    path('Myprofile/', Myprofile, name='Myprofile'),
    path('editProfile/', profileChange, name='editProfile'),
    path('saveEditProfile/', saveEditProfile, name='saveEditProfile'),
    path('mySupport/', mySupport, name='mySupport'),
    path('changeMyPassword/', resetPassword, name='changeMyPassword'),
    path('saveChangeMyPassword/', saveChangeMyPassword, name='saveChangeMyPassword'),
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
