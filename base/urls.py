from unicodedata import name
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('room/<str:pk>/', views.room, name='room'),
  path('room-form/', views.room_form, name='room_form'),
  path('room-update/<str:pk>/', views.update_room, name='update_room'),
  path('room-delete/<str:pk>/', views.delete_room, name='delete_room'),
  path('login/', views.login_reg, name='login_reg'),
  path('logout/', views.logout_view, name='logout')
]