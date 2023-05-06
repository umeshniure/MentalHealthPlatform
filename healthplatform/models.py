from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

GENDER = (
    ("M", "Male"),
    ("F", "Female"),
    ("O", "Other")
)


def upload_location(instance, filename):
    file_path = f'blog/{instance.author.id}/{instance.title}-{filename}'.format(author_id=str(instance.author_id),
                                                                                title=str(instance.title),
                                                                                filename=filename)
    return file_path


# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=100)
    phone = models.IntegerField(null=True)
    dob = models.DateField(null=True)
    gender = models.CharField(max_length=2, choices=GENDER, null=True)
    password = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    is_superuser= models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.first_name + self.last_name

    class Meta:
        ordering = ['-created_on']


class Doctor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    license = models.IntegerField()
    education = models.CharField(max_length=50)
    speciality = models.CharField(max_length=50)
    rate = models.IntegerField()
    # experience = models.CharField(max_length=50)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return f"{self.user_id}"


class Patient(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return f"{self.user_id}"


class Schedule(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='schedule')
    date = models.DateField()
    time = models.TimeField()
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']


STATUS = (
    ("P", "Pending"),
    ("A", "Accepted"),
    ("C", "Completed"),
    ("D", "Declined")
)


class Appointment(models.Model):
    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='patientid')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='doctorid')
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name='schedule')
    status = models.CharField(max_length=2, choices=STATUS, default='P')
    problem_statement = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']


class AppointmentRequest(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.appointment} - {self.doctor}"


class Review(models.Model):
    # user needs to be added
    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True)
    star = models.IntegerField(default=0)
    comment = models.TextField(null=True, blank=True)
    createdDate = models.DateTimeField(auto_now_add=True)
    updatedDate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment
