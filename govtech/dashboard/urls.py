from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import multi_step_registration, individual_reg, index, authlogout, \
    Myprofile, profileChange, saveEditProfile, mySupport, resetPassword, saveChangeMyPassword, dashboard_view  # DashboardData

urlpatterns = [
    # path("", views.home, name="home"),
    path('SoftwareFirm/', multi_step_registration, name='multi_step'),
    path('step/<int:step>/', multi_step_registration, name='multi_step'),
    path('individual/', individual_reg, name='individual_reg'),
    path('', dashboard_view, name='dashboard_view'),
    path("index/", index, name="index"),
    path("authlogout/", authlogout, name="authlogout"),
    path('Myprofile/', Myprofile, name='Myprofile'),
    path('editProfile/', profileChange, name='editProfile'),
    path('saveEditProfile/', saveEditProfile, name='saveEditProfile'),
    path('mySupport/', mySupport, name='mySupport'),
    path('changeMyPassword/', resetPassword, name='changeMyPassword'),
    path('saveChangeMyPassword/', saveChangeMyPassword, name='saveChangeMyPassword'),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)















'''
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    path('newsletter/', include('newsletter.urls')),
]
'''
