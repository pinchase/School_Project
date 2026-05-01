from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
import random


phone_validator = RegexValidator(
    regex=r'^\+[1-9]\d{1,14}$',
    message='Phone number must use E.164 format, for example +254712345678.',
)


def generate_appointment_number():
    while True:
        number = random.randint(100000000, 999999999)
        if not Appointment.objects.filter(appointmentnumber=number).exists():
            return number


class CustomUser(AbstractUser):
    class UserType(models.TextChoices):
        ADMIN = '1', 'admin'
        DOCTOR = '2', 'doc'
        PATIENT = '3', 'patient'

    user_type = models.CharField(
        choices=UserType.choices,
        max_length=50,
        default=UserType.ADMIN,
    )
    profile_pic = models.ImageField(upload_to='profile_pic', blank=True, null=True)

class Specialization(models.Model):
    sname = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.sname
   
    

class DoctorReg(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
   
    mobilenumber = models.CharField(max_length=16, validators=[phone_validator])
    specialization_id = models.ForeignKey(Specialization, on_delete=models.CASCADE)
    regdate_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.admin:
            return f"{self.admin.first_name} {self.admin.last_name} - {self.mobilenumber}"
        else:
            return f"User not associated - {self.mobilenumber}"

class Appointment(models.Model):
    class Status(models.TextChoices):
        NEW = '0', 'New'
        APPROVED = 'Approved', 'Approved'
        CANCELLED = 'Cancelled', 'Cancelled'
        COMPLETED = 'Completed', 'Completed'

    appointmentnumber = models.PositiveIntegerField(
        default=generate_appointment_number,
        unique=True,
        db_index=True,
    )
    fullname = models.CharField(max_length=250)
    mobilenumber = models.CharField(max_length=16, validators=[phone_validator])
    email = models.EmailField(max_length=100)
    
    date_of_appointment = models.DateField()  
    time_of_appointment = models.TimeField()  
    
    doctor_id = models.ForeignKey(DoctorReg, on_delete=models.CASCADE)
    additional_msg = models.TextField(blank=True)

    remark = models.CharField(max_length=250, default="0")
    status = models.CharField(
        choices=Status.choices,
        max_length=20,
        default=Status.NEW,
    )
    prescription = models.TextField(blank=True, default="")
    recommendedtest = models.TextField(blank=True, default="")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        super().clean()
        
        conflict = Appointment.objects.filter(
            doctor_id=self.doctor_id,
            date_of_appointment=self.date_of_appointment,
            time_of_appointment=self.time_of_appointment
        ).exclude(id=self.id)

        if conflict.exists():
            raise ValidationError("The doctor is already booked at this time. Please select another slot.")

    def save(self, *args, **kwargs):
        if not self.appointmentnumber:
            self.appointmentnumber = generate_appointment_number()
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Appointment #{self.appointmentnumber} - {self.fullname}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['doctor_id', 'date_of_appointment', 'time_of_appointment'],
                name='unique_doctor_appointment_slot',
            ),
        ]

class Page(models.Model):
    pagetitle = models.CharField(max_length=250)
    address = models.CharField(max_length=250)
    aboutus = models.TextField()
    email = models.EmailField(max_length=200)
    mobilenumber = models.CharField(max_length=16, blank=True, validators=[phone_validator])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.pagetitle
 
