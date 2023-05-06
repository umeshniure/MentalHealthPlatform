from django.forms import ModelForm
from .models import Doctor, Patient
from .models import Appointment, Review
from django import forms

# Forms.py is not used anywhere. can be safely deleted

from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser


class AppointmentForm(ModelForm):
    class Meta:
        model = Appointment
        fields = '__all__'


class DoctorForm(ModelForm):
    class Meta:
        model = Doctor
        fields = '__all__'


class PatientForm(ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = '__all__'
