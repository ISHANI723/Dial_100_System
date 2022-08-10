from django.contrib import admin
from django.urls import path
from form1 import views

urlpatterns = [
    path('', views.index,name='index'),
    path('form2', views.form2),
]
