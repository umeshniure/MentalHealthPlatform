from django.contrib import messages
from django.template import loader
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate

from healthplatform.forms import AppointmentForm
from .models import CustomUser, Doctor, Patient, Review, Appointment, AppointmentRequest
from django.contrib.auth.decorators import login_required

from .forms import PatientForm, DoctorForm

import csv


# Create your views here.

# index page for the web app
# also an default page for when there is no parameters in the path of url
def home(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())

# for registering the doctor
def register_doctor(request):

    page = 'register_doctor'
    form = DoctorForm()

    if request.method == 'POST':
        
        form = DoctorForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login/')
        
    context = {'page' : page, 'form' : form}
    return render(request, 'register_doctor.html', context)

# allows user to check detail on the appoinment, user ust be logged in to perform it
@login_required(login_url="login")
def appoinment(request, pk):
    appointment = None
    appointment = Appointment.objects.get(id = pk)
    
    context = {'appointment' : appointment}
    return render(request, 'appointment.html', context)

# for registering as patient
def register_patient(request):

    page = 'register_patient'
    form = PatientForm()

    if request.method == 'POST':
        
        form = PatientForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login/')
        
    context = {'page' : page, 'form' : form}
    return render(request, 'register_patient.html', context)

# allows to make appoinment
@login_required(login_url="login")
def make_appointment(request, doctor_id):
    doctor = Doctor.objects.get(id=doctor_id)

    # if form submitted matches the model and thus valid data is saved to database
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            # Create a new Appointment object based on the form data
            appointment = form.save(commit=False)
            appointment.patient = request.user
            appointment.doctor = doctor
            appointment.save()
            return redirect('home')
        else:
            return redirect('make_appoinment')
    else:
        # if the user is asking for appointment form
        form = AppointmentForm()
        return render(request, 'make_appointment.html', {'doctor': doctor, 'form': form})

# doctor to accept or decline the appoinment request of the user
@login_required(login_url="login")
def appointment_requests(request):
    doctor = request.user.doctor
    requests = AppointmentRequest.objects.filter(doctor=doctor, accepted=False)

    if request.method == 'POST':
        request_id = request.POST.get('request_id')
        accepted = request.POST.get('accepted') == 'True'

        # if request is declined save reason why
        if accepted == 'False':
            reason = request.POST.get('reason')

        request = get_object_or_404(AppointmentRequest, id=request_id)
        request.accepted = accepted
        request.reason = reason
        request.save()

    return render(request, 'appointment_requests.html', {'requests': requests})


# provides appoinments data according to the user
@login_required(login_url="login")
def user_appointments(request):
    if request.user.is_doctor:
        appointments = Appointment.objects.filter(doctor=request.user)
    else:
        appointments = Appointment.objects.filter(patient=request.user)

    # both users appoinment can be shown on the same file(page)
    return render(request, 'user_appointments.html', {'appointments': appointments})

# a way for user to provide review for the doctor
@login_required(login_url="login")
def write_review(request, doctor_id):
    if request.method == 'POST':
        star = request.POST['star']
        comment = request.POST['comment']
        patient = request.user.patient
        doctor = Doctor.objects.get(id=doctor_id)
        review = Review.objects.create(patient=patient, doctor=doctor, star=star, comment=comment)
        messages.success(request, 'Your review has been submitted!')
        return redirect('doctor_detail', doctor_id=doctor_id)

    return render(request, 'add_review.html', {'doctor_id': doctor_id})


def export_doctor_data(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="MentalHealthPlatform\healthplatform\Doctor_Data.csv"'

    # Query the database for the doctor data
    doctors = Doctor.objects.all()

    # Write the doctor data to the CSV file
    writer = csv.writer(response)
    writer.writerow(["Doctor_id", "Name", "Speciality", "Price", "Location"])
    for doctor in doctors:
        writer.writerow([doctor.id, doctor.user.name, doctor.speciality, doctor.price, doctor.user.address])

    return response

def export_appoinment_data(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="MentalHealthPlatform\healthplatform\data.csv"'

    # Query the database for the reviews data
    reviews = Review.objects.all()

    # Write the doctor data to the CSV file
    writer = csv.writer(response)
    writer.writerow(["Doctor_id", "Patient ID", "Problem" ,"Appointment Rating"])
    for review in reviews:
        writer.writerow([review.appointment.doctor.id, review.appointment.patient.id, review.appointment.problem_statement, review.star])

    return response



# the user who wrote the review may delete the review as well
@login_required(login_url="login")
def deleteReview(request, pk):
    review = Review.objects.get(id=pk)

    if request.user != review.user:
        return HttpResponse('You are not owner of this review!!')

    if request.method == 'POST':
        review.delete()
        return redirect('home')
    context = {'obj': review}
    return render(request, 'delete.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def login(request):
    page = 'login'

    # if request.user.is_authenticated:
    #     return redirect('home')

    if request.method == 'POST':
        print("Hello!!")
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)
        print(email, password)
        if user is not None:
            return redirect('home')
        else:
            messages.error(request, "Incorrect email or password combination")
            return redirect('login')

    context = {'page': page}
    return render(request, 'login.html', context)

# from django.shortcuts import render

# # Create your views here.
# def test(request):
#     '''
#         Description:
#             This is a function that is used to prevent csrf attack
        
#             params:
#                 request: HttpRequest, required
#                 id: int, optional
            
#             return:
#                 None if id is not provided. HttpRequest is id is not None

#     '''
