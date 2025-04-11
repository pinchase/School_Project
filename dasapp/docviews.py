from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import CustomUser, DoctorReg, Appointment

def DOCSIGNUP(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        mobilenumber = request.POST.get('mobilenumber')
        specialization_id = request.POST.get('specialization_id')

        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            user_type=2
        )

        DoctorReg.objects.create(
            admin=user,
            mobilenumber=mobilenumber,
            specialization_id_id=specialization_id
        )
        return redirect('login')
    return render(request, 'doctor/doctorsignup.html')

@login_required
def DOCTORHOME(request):
    return render(request, 'doctor/doctorhome.html')

@login_required
def View_Appointment(request):
    doctor = DoctorReg.objects.get(admin=request.user)
    appointments = Appointment.objects.filter(doctor_id=doctor)
    return render(request, 'doctor/viewappointment.html', {'appointments': appointments})

@login_required
def Patient_Appointment_Details(request, id):
    appointment = Appointment.objects.get(id=id)
    return render(request, 'doctor/patientappointmentdetails.html', {'appointment': appointment})

@login_required
def Patient_Appointment_Details_Remark(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        remark = request.POST.get('remark')
        appointment = Appointment.objects.get(id=id)
        appointment.remark = remark
        appointment.save()
        return redirect('view_appointment')
    return redirect('view_appointment')

@login_required
def Patient_Approved_Appointment(request):
    doctor = DoctorReg.objects.get(admin=request.user)
    appointments = Appointment.objects.filter(doctor_id=doctor, status='1')
    return render(request, 'doctor/patientapprovedappointment.html', {'appointments': appointments})

@login_required
def Patient_Cancelled_Appointment(request):
    doctor = DoctorReg.objects.get(admin=request.user)
    appointments = Appointment.objects.filter(doctor_id=doctor, status='2')
    return render(request, 'doctor/patientcancelledappointment.html', {'appointments': appointments})

@login_required
def Patient_New_Appointment(request):
    doctor = DoctorReg.objects.get(admin=request.user)
    appointments = Appointment.objects.filter(doctor_id=doctor, status='0')
    return render(request, 'doctor/patientnewappointment.html', {'appointments': appointments})

@login_required
def Patient_List_Approved_Appointment(request):
    doctor = DoctorReg.objects.get(admin=request.user)
    appointments = Appointment.objects.filter(doctor_id=doctor, status='1')
    return render(request, 'doctor/patientlistappointment.html', {'appointments': appointments})

@login_required
def DoctorAppointmentList(request, id):
    doctor = DoctorReg.objects.get(id=id)
    appointments = Appointment.objects.filter(doctor_id=doctor)
    return render(request, 'doctor/doctorappointmentlist.html', {'appointments': appointments})

@login_required
def Patient_Appointment_Prescription(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        prescription = request.POST.get('prescription')
        appointment = Appointment.objects.get(id=id)
        appointment.prescription = prescription
        appointment.save()
        return redirect('view_appointment')
    return redirect('view_appointment')

@login_required
def Patient_Appointment_Completed(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        appointment = Appointment.objects.get(id=id)
        appointment.status = '3'
        appointment.save()
        return redirect('view_appointment')
    return redirect('view_appointment')

@login_required
def Search_Appointments(request):
    if request.method == 'POST':
        search_query = request.POST.get('search')
        doctor = DoctorReg.objects.get(admin=request.user)
        appointments = Appointment.objects.filter(
            doctor_id=doctor,
            fullname__icontains=search_query
        )
        return render(request, 'doctor/viewappointment.html', {'appointments': appointments})
    return redirect('view_appointment')

@login_required
def Between_Date_Report(request):
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        doctor = DoctorReg.objects.get(admin=request.user)
        appointments = Appointment.objects.filter(
            doctor_id=doctor,
            date_of_appointment__range=[start_date, end_date]
        )
        return render(request, 'doctor/betweendatereport.html', {'appointments': appointments})
    return render(request, 'doctor/betweendatereport.html') 