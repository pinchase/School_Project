from datetime import date, time, timedelta

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from dasapp.models import Appointment, CustomUser, DoctorReg, Specialization
from dasapp.utils import normalize_phone_number


class AppointmentModelTests(TestCase):
    def setUp(self):
        self.specialization = Specialization.objects.create(sname='Cardiology')
        self.doctor_user = CustomUser.objects.create_user(
            username='doctor',
            email='doctor@example.com',
            password='testpass123',
            user_type=CustomUser.UserType.DOCTOR,
        )
        self.doctor = DoctorReg.objects.create(
            admin=self.doctor_user,
            mobilenumber='+254712345678',
            specialization_id=self.specialization,
        )

    def test_duplicate_doctor_slot_is_rejected(self):
        appointment_date = date.today() + timedelta(days=2)
        Appointment.objects.create(
            fullname='Patient One',
            mobilenumber='+254700000001',
            email='one@example.com',
            date_of_appointment=appointment_date,
            time_of_appointment=time(9, 0),
            doctor_id=self.doctor,
        )

        duplicate = Appointment(
            fullname='Patient Two',
            mobilenumber='+254700000002',
            email='two@example.com',
            date_of_appointment=appointment_date,
            time_of_appointment=time(9, 0),
            doctor_id=self.doctor,
        )

        with self.assertRaises(ValidationError):
            duplicate.full_clean()

    def test_appointment_number_is_generated(self):
        appointment = Appointment.objects.create(
            fullname='Patient One',
            mobilenumber='+254700000001',
            email='one@example.com',
            date_of_appointment=date.today() + timedelta(days=2),
            time_of_appointment=time(9, 0),
            doctor_id=self.doctor,
        )

        self.assertGreaterEqual(appointment.appointmentnumber, 100000000)


class PhoneNumberTests(TestCase):
    def test_kenyan_numbers_are_normalized_to_e164(self):
        self.assertEqual(normalize_phone_number('0712345678'), '+254712345678')
        self.assertEqual(normalize_phone_number('712345678'), '+254712345678')
        self.assertEqual(normalize_phone_number('+254712345678'), '+254712345678')


class RoleAccessTests(TestCase):
    def setUp(self):
        self.specialization = Specialization.objects.create(sname='Dermatology')
        self.admin_user = CustomUser.objects.create_user(
            username='adminuser',
            email='admin@example.com',
            password='testpass123',
            user_type=CustomUser.UserType.ADMIN,
        )
        self.doctor_user = CustomUser.objects.create_user(
            username='doctoruser',
            email='doc@example.com',
            password='testpass123',
            user_type=CustomUser.UserType.DOCTOR,
        )
        self.doctor = DoctorReg.objects.create(
            admin=self.doctor_user,
            mobilenumber='+254712345678',
            specialization_id=self.specialization,
        )

    def test_doctor_cannot_access_admin_home(self):
        self.client.force_login(self.doctor_user)
        response = self.client.get(reverse('admin_home'))

        self.assertRedirects(response, reverse('doctor_home'))

    def test_admin_cannot_access_doctor_home(self):
        self.client.force_login(self.admin_user)
        response = self.client.get(reverse('doctor_home'))

        self.assertRedirects(response, reverse('index'))
