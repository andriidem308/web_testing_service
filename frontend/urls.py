from django.contrib import admin
from django.urls import path, include

from frontend.views import index

urlpatterns = [
    path('react/', index, name='react'),
]
