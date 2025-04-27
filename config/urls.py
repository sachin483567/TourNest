"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
     path("",TemplateView.as_view (template_name="index.html"),name="home"),
     path("login/",TemplateView.as_view (template_name="login.html"),name="login"),
     path("register/",TemplateView.as_view (template_name="register.html"),name="register"),
     path("host_profile/",TemplateView.as_view (template_name="host_profile.html"),name="host_profile"),
     path("user_profile/",TemplateView.as_view (template_name="user_profile.html"),name="user_profile"),
     
     path("",include('location.urls'),name="location"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)