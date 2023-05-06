from django.contrib import messages
from django.template import loader
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.views.generic import ListView
from django.contrib.auth import login, logout, authenticate

from healthplatform.forms import AppointmentForm
from .models import CustomUser, Doctor, Patient, Review, Appointment, AppointmentRequest
from django.contrib.auth.decorators import login_required

from .forms import PatientForm, DoctorForm


# Create your views here.

# index page for the web app
# also an default page for when there is no parameters in the path of url
def home(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())


class PatientDashboard(ListView):
    model = Doctor
    queryset = Doctor.objects.select_related('user').order_by('-created_on')
    template_name = 'patientDashboard.html'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        return {'doctors': Doctor.objects.select_related('user').order_by('-created_on')}


def doctor_dashboard(request):
    template = loader.get_template('doctor/doctorDashboard.html')
    return HttpResponse(template.render())


# for registering the doctor
def register_doctor(request):
    if request.method == 'POST':
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        dob = request.POST['dob']
        address = request.POST['address']
        gender = request.POST['gender']

        license = request.POST['license']
        education = request.POST['education']
        speciality = request.POST['speciality']
        rate = request.POST['rate']

        user = CustomUser.objects.create_user(email=email, password=password, first_name=first_name,
                                              last_name=last_name, dob=dob, phone=phone, address=address, gender=gender)

        Doctor.objects.create(user_id=user.id, license=license, education=education, speciality=speciality, rate=rate)
        return redirect('home')

    return render(request, 'doctor/doctorRegistration.html', {'page': register_doctor})


# allows user to check detail on the appoinment, user ust be logged in to perform it
@login_required(login_url="login")
def appoinment(request, pk):
    appointment = None
    appointment = Appointment.objects.get(id=pk)

    context = {'appointment': appointment}
    return render(request, 'appointment.html', context)


# for registering as patient
def register_patient(request):
    if request.method == 'POST':
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        dob = request.POST['dob']
        address = request.POST['address']
        gender = request.POST['gender']
        user = CustomUser.objects.create_user(email=email, password=password, first_name=first_name,
                                              last_name=last_name, dob=dob, phone=phone, address=address, gender=gender)
        # temp_user = user.save()

        Patient.objects.create(user_id=user.id)
        return redirect('home')
    else:
        return render(request, 'patientRegister.html', {'page': register_patient})


# allows to make appoinment
@login_required(login_url="login")
def make_appointment(request, doctor_id):
    page = "appointment"
    doctor = Doctor.objects.get(id=doctor_id)
    print("Hello")
    # if form submitted matches the model and thus valid data is saved to database
    if request.method == 'POST':
        problem_statement = "Paranoia"
        problem_description = request.POST['problem_description']
        date = request.POST['date']
        time = request.POST['time']
        print("+++++++++++++++++++")
        print(time)
        print(date)
        print(doctor.id)
        print(request.user.id)
        patient = Patient.objects.get(id=request.user.id)
        # patient = Patient.objects.select_related(request.user.id)
        print(patient.id)
        Appointment.objects.create(patient=patient, doctor=doctor, status='P',
                                   problem_statement=problem_statement, problem_description=problem_description,
                                   date=date, time=time)

        print("Successfullt appinted")
        return redirect('view_user_appointment')
    else:
        context = {'obj': page, 'doctor': doctor}
        return render(request, 'patientBookAppointment.html', context)
        # if the user is asking for appointment form
        # form = AppointmentForm()
        # return render(request, 'make_appointment.html', {'doctor': doctor, 'form': form})


@login_required
def AppoinmentPage(request, user_id):
    appoinment = None
    appoinment = Appointment.objects.all()
    return render(request, 'appointment.html', {'appointment': appoinment})


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
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)
        print(user)
        if user is not None:
            if hasattr(user, 'doctor'):  # Check if the user is a doctor
                return redirect('doctor_dashboard')
            elif hasattr(user, 'patient'):  # Check if the user is a patient
                return redirect('patient_dashboard')
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
