from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register_doctor/', views.register_doctor, name='register_doctor'),
    path('register_patient/', views.register_patient, name='register_patient'),
    path('login/', views.login, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('request_appointment', views.AppointmentForm, name='request_appointment'),
]