from django.contrib import admin
from django.urls import path
from form1 import views

urlpatterns = [
    path('', views.index,name='index'),
    path('form2', views.form2, name='Supervisor'),
    path('movetohistory/<int:case_id>', views.move_to_history, name='MoveToHistory'),
    path('add_frv', views.index,name='AddFrv'),
]
