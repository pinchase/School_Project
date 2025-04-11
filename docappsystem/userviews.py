from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from dasapp.models import DoctorReg,Specialization,CustomUser,Appointment,Page
import random
from datetime import datetime
from django.contrib import messages
from django.db.models import Q
from dasapp.utils import send_sms



def USERBASE(request):
    
    return render(request, 'userbase.html')

def Index(request):
    doctorview = DoctorReg.objects.all()
    page = Page.objects.all()

    context = {'doctorview': doctorview,
    'page':page,
    }
    return render(request, 'index.html',context)




def create_appointment(request):
    doctorview = DoctorReg.objects.all()
    page = Page.objects.all()

    if request.method == "POST":
        appointmentnumber = random.randint(100000000, 999999999)
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        mobilenumber = request.POST.get('mobilenumber')
        # Format phone number to E.164 format
        if not mobilenumber.startswith('+'):
            if mobilenumber.startswith('0'):
                mobilenumber = '+254' + mobilenumber[1:]  # Assuming Kenya numbers
            else:
                mobilenumber = '+254' + mobilenumber  # Add country code if missing
        date_of_appointment = request.POST.get('date_of_appointment')
        time_of_appointment = request.POST.get('time_of_appointment')
        doctor_id = request.POST.get('doctor_id')
        additional_msg = request.POST.get('additional_msg')

        try:
            appointment_date = datetime.strptime(date_of_appointment, '%Y-%m-%d').date()
            today_date = datetime.now().date()

            if appointment_date <= today_date:
                messages.error(request, "Please select a future date for your appointment.")
                return redirect('appointment')
        except ValueError:
            messages.error(request, "Invalid date format")
            return redirect('appointment')

        doc_instance = DoctorReg.objects.get(id=doctor_id)

        # Save appointment
        appointmentdetails = Appointment.objects.create(
            appointmentnumber=appointmentnumber,
            fullname=fullname,
            email=email,
            mobilenumber=mobilenumber,
            date_of_appointment=date_of_appointment,
            time_of_appointment=time_of_appointment,
            doctor_id=doc_instance,
            additional_msg=additional_msg
        )

        # Send SMS confirmation
        sms_message = f"Hello {fullname}, your appointment with Dr. {doc_instance.admin.first_name} {doc_instance.admin.last_name} is confirmed for {date_of_appointment} at {time_of_appointment}."
        try:
            sms_status = send_sms(mobilenumber, sms_message, sender_name=f"Dr.{doc_instance.admin.first_name}")
            if "error" in sms_status.lower():
                messages.error(request, f"Appointment saved, but SMS failed to send. Error: {sms_status}")
            else:
                messages.success(request, "Appointment confirmed! SMS sent successfully.")
        except Exception as e:
            messages.error(request, f"Appointment saved, but SMS failed to send. Error: {str(e)}")

        return redirect('appointment')

    context = {'doctorview': doctorview, 'page': page}
    return render(request, 'appointment.html', context)


def User_Search_Appointments(request):
    query = request.GET.get('query', '').strip()

    if query:
        patient = Appointment.objects.filter(
            Q(fullname__icontains=query) | Q(appointmentnumber__icontains=query)
        )
        messages.info(request, f"Search results for '{query}'")
    else:
        patient = None
        messages.warning(request, "No search term provided.")

    return render(request, 'search-appointment.html', {'patient': patient, 'query': query})

def View_Appointment_Details(request,id):
    page = Page.objects.all()
    patientdetails=Appointment.objects.filter(id=id)
    context={'patientdetails':patientdetails,
    'page': page

    }

    return render(request,'user_appointment-details.html',context)




