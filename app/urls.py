from django.contrib import admin
from django.urls import path
from app import views

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path("",views.index,name='index'),
    path('login/',views.login_user,name ='login_user'),
    path('register/',views.Register_user,name ='Register_user'),
    path('view/',views.view_data,name ='view_data'),
    path('final/',views.final_page,name ='final_page'),
    path('home/',views.home,name ='home'),
    path('contact/',views.contact,name ='contact'),

    path('drf_view/', views.drf_view, name='drf_view'),
    path('logout/', views.logout_v, name='logout_v'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("send-otp/", views.send_otp, name="send_otp"),
    path("verify-otp/", views.verify_otp, name="verify_otp"),
    path('protected/', views.protected_view, name='protected_view'),
  

    
    ]