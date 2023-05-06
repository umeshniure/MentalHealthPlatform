from django.urls import path, include

from django.contrib.auth.views import LoginView
from .forms import CustomAuthenticationForm
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register_doctor/', views.register_doctor, name='register_doctor'),
    path('register_patient/', views.register_patient, name='register_patient'),
    path('login/', views.login, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('patient_dashboard/', views.PatientDashboard.as_view(), name='patient_dashboard'),
    path('doctor_dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('create_appointment/<int:doctor_id>', views.make_appointment, name='create_appointment'),
    path('view_user_appointment/', views.user_appointments_list, name="view_user_appointment"),
    path('view_doctor_appointment/', views.doctor_appointments_list, name="view_doctor_appointment"),

    path('request_appointment', views.AppointmentForm, name='request_appointment'),
    # path('view_appointment', views.user_appointments, name="view_appointment"),
    path('deleteReview/<str:pk>/', views.deleteReview, name = "deleteReview"),
<<<<<<< HEAD
    # path('deleteAppointment/<str:pk>/', views.deleteAppointment, name = "deleteAppointment"),
=======
<<<<<<< HEAD
    path('deleteAppointment/<str:pk>/', views.deleteAppointment, name = "deleteAppointment"),
>>>>>>> frontend
=======
    # path('deleteAppointment/<str:pk>/', views.deleteAppointment, name = "deleteAppointment"),
    path('export_doctor_data/', views.export_doctor_data, name='export_doctor_data'),
    path('export_appointment_data/', views.export_appoinment_data, name='export_appointment_data'),
>>>>>>> f01d1198e39a9c5d604222125a414b565327a2cc
>>>>>>> SGE
    path('login/', LoginView.as_view(authentication_form=CustomAuthenticationForm), name='login'),


]
