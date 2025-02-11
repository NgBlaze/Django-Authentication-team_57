from django.contrib import admin
from django.urls import path,include
from . import views
from .views import profile

urlpatterns = [
    path('', views.home, name="home"),
    path('signin', views.signin, name="signin"),
    path('register', views.register, name="register"),
    path('signout', views.signout, name="signout"),
    path("contact", views.contact, name="contact"),
    path("password_reset", views.password_reset_request, name="password_reset"),
    path('profile', profile, name='users-profile'),
]
