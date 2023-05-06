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
<<<<<<< HEAD
    path('patient_dashboard/', views.PatientDashboard.as_view(), name='patient_dashboard'),
    path('doctor_dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('create_appointment/<int:doctor_id>', views.make_appointment, name='create_appointment'),
    path('view_user_appointment/', views.user_appointments, name="view_user_appointment"),
=======
    path('request_appointment', views.AppointmentForm, name='request_appointment'),
    path('view_appointment', views.user_appointments, name="view_appointment"),
    path('deleteReview/<str:pk>/', views.deleteReview, name = "deleteReview"),
    path('deleteAppointment/<str:pk>/', views.deleteAppointment, name = "deleteAppointment"),
>>>>>>> frontend
    path('login/', LoginView.as_view(authentication_form=CustomAuthenticationForm), name='login'),


]
