from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import DoctorReg, Appointment, Page

def USERBASE(request):
    return render(request, 'user/userbase.html')

def Index(request):
    doctors = DoctorReg.objects.all()
    page = Page.objects.first()
    return render(request, 'user/index.html', {'doctors': doctors, 'page': page})

@login_required
def create_appointment(request):
    if request.method == 'POST':
        fullname = request.POST.get('fullname')
        mobilenumber = request.POST.get('mobilenumber')
        email = request.POST.get('email')
        date_of_appointment = request.POST.get('date_of_appointment')
        time_of_appointment = request.POST.get('time_of_appointment')
        doctor_id = request.POST.get('doctor_id')
        additional_msg = request.POST.get('additional_msg')

        appointment = Appointment.objects.create(
            fullname=fullname,
            mobilenumber=mobilenumber,
            email=email,
            date_of_appointment=date_of_appointment,
            time_of_appointment=time_of_appointment,
            doctor_id_id=doctor_id,
            additional_msg=additional_msg,
            status='0'
        )
        return redirect('viewappointmentdetails', id=appointment.id)
    
    doctors = DoctorReg.objects.all()
    return render(request, 'user/appointment.html', {'doctors': doctors})

@login_required
def User_Search_Appointments(request):
    if request.method == 'POST':
        search_query = request.POST.get('search')
        appointments = Appointment.objects.filter(
            fullname__icontains=search_query,
            email=request.user.email
        )
        return render(request, 'user/viewappointment.html', {'appointments': appointments})
    return redirect('index')

@login_required
def View_Appointment_Details(request, id):
    appointment = Appointment.objects.get(id=id)
    return render(request, 'user/viewappointmentdetails.html', {'appointment': appointment}) 