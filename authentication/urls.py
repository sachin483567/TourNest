# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path
from . import views

app_name = 'authentication'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('host-profile/', views.host_profile_view, name='host_profile'),
    path('user-profile/', views.user_profile_view, name='user_profile'),
    path('become-host/', views.become_host_view, name='become_host'),
    # Other authentication URLs...
]