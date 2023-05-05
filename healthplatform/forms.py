from django.forms import ModelForm
from .models import Doctor, Patient
from .models import Appointment, Review


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