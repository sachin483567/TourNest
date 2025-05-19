# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path
from .views import login_view, register_user
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('login/', login_view, name="login"),
    path('register/', register_user, name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('become-host/', views.register_host, name='register_host'),
    path('host-login/', views.host_login, name='host_login'),
    path('host/dashboard/', views.host_dashboard, name='host_dashboard'),
]
