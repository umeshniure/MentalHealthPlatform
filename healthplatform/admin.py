from django.contrib import admin
from .models import CustomUser, Doctor, Patient, Schedule, Appointment, Review

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Doctor)
admin.site.register(Review)
admin.site.register(Patient)
admin.site.register(Schedule)
admin.site.register(Appointment)
