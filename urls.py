from django.contrib import admin
from django.urls import path 
from . import views

urlpatterns = [
    path('', views.index),
    path("success", views.success),
    path("travels", views.travels),
    path("logout", views.logout),
    path("login", views.login),
    path("travels/add", views.add),
    path("travels/upload", views.uploadTrip),
    path("destination/<tripID>", views.tripID),
    path("travels/jointrip/<tripID>", views.join)
]