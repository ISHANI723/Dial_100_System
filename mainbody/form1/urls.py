from django.contrib import admin
from django.urls import path
from form1 import views

urlpatterns = [
    path('form1', views.index,name='index'),
    path('form2', views.form2, name='Supervisor'),
    path('', views.login_view, name='home'),
    path('signup', views.signup_view, name='signup'),
    path('menu', views.menu_view, name='menu'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('draw',views.newroad,name='draw'),
    path('movetohistory/<int:case_id>', views.move_to_history, name='MoveToHistory'),
    path('add_frv', views.create_frv ,name='AddFrv'),
    path('driver', views.driver, name='driver'),
    path('location/case/get', views.get_case_location, name='GetCaseLocation'),
    path('location/case/set', views.set_case_location, name='SaveCaseLocation'),
    path('assignfrv', views.assign_frv, name='AssignFRV' ),
    path('road', views.roadlayer, name='RoadLayer' ),
]
