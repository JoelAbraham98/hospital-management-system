from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
import datetime
from django.contrib.auth.models import AbstractUser


# Create your models here.

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    profile_picture = models.ImageField(upload_to='doctor_profiles/', blank=True, null=True)

    def __str__(self):
        return f"Dr. {self.first_name} {self.last_name}"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_user_name(self):
        return self.user.get_full_name() if self.user else self.get_full_name()
    def get_full_name(self):
        return f"Dr. {self.first_name} {self.last_name}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(default='')
    is_doctor = models.BooleanField(default=False)
    doctor = models.OneToOneField(Doctor, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.username
    


class Patient(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    TIME_CHOICES = [
        ('9-10', '9-10'),
        ('10-11', '10-11'),
        ('11-12', '11-12'),
        ('1-2', '1-2'),
        ('2-3', '2-3'),
        ('3-4', '3-4'),
        ('4-5', '4-5'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    appointment_date = models.DateTimeField(null=True, blank=True)
    slot = models.CharField(max_length=5, choices=TIME_CHOICES, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    def get_gender_display(self):
        return dict(self.GENDER_CHOICES)[self.gender]


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('skipped', 'Skipped'),
    ]

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    appointment_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    
    description = models.TextField(blank=True, null=True)
    description_file = models.FileField(upload_to='appointment_descriptions/', blank=True, null=True)

    def __str__(self):
        return f"Appointment for {self.patient} with {self.doctor} at {self.appointment_time}"

class MedicalRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, null=True, blank=True)
    record_date = models.DateField()

    def __str__(self):
        return f"Medical Record for {self.patient} by {self.doctor} on {self.record_date}"