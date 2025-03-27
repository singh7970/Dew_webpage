from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path("",views.index,name='index'),
    path('login/',views.login_user,name ='login_user'),
    path('register/',views.Register_user,name ='Register_user'),
    path('view/',views.view_data,name ='view_data'),
    path('final/',views.final_page,name ='final_page'),
    path('home/',views.home,name ='home'),
    # path('drf_view/', views.drf_view, name='drf_view'),
    path('logout/', views.logout_v, name='logout_v'),
    path('contact/',views.contact,name ='contact'),
    
    ]