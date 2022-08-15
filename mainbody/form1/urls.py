from django.contrib import admin
from django.urls import path
from form1 import views

urlpatterns = [
    path('form1', views.index,name='index'),
    path('form2', views.form2, name='Supervisor'),
    path('home', views.home, name='home'),
    path('signup', views.signup_view, name='signup'),
    path('menu', views.menu_view, name='menu'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('movetohistory/<int:case_id>', views.move_to_history, name='MoveToHistory'),
    path('add_frv', views.create_frv ,name='AddFrv'),
    path('driver', views.driver, name='driver'),
]
