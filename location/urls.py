from django.contrib import admin
from django.urls import path,include
from django.views.generic import TemplateView

from .views import browse, productDetails

urlpatterns = [
    path('browse/', browse , name='browse'),
    path("details/<int:location_id>",productDetails,name="locationDetails"),
]