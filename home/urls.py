from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.home,name="home"), 
    path('about/',views.about1,name="about1"),
    path('about/<str:authSlug>',views.about,name="about"),
    path('contact',views.contact,name="contact"), 
    path('search',views.search,name="search"),
    path('signup',views.handleSignup,name="handleSignup"),
    path('login',views.handlelogin,name="handlelogin"),
    path('logout',views.handlelogout,name="handlelogout"),
]