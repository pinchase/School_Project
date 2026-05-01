from django.shortcuts import render,redirect,HttpResponse
from dasapp.models import Specialization,DoctorReg,Appointment,Page
from django.contrib import messages
from datetime import datetime
from dasapp.decorators import admin_required
from dasapp.utils import normalize_phone_number

@admin_required
def ADMINHOME(request):
    doctor_count = DoctorReg.objects.all().count()
    specialization_count = Specialization.objects.all().count()
    context = {
        'doctor_count':doctor_count,
        'specialization_count':specialization_count,

    } 
    return render(request,'admin/adminhome.html',context)

@admin_required
def SPECIALIZATION(request):
    if request.method == "POST":
        specializationname = request.POST.get('specializationname')
        specialization =Specialization(
            sname=specializationname,
        )
        specialization.save()
        messages.success(request,'Specialization  Added Succeesfully!!!')
        return redirect("add_specilizations")
    return render(request,'admin/specialization.html')

@admin_required
def MANAGESPECIALIZATION(request):
    specialization = Specialization.objects.all()
    context = {'specialization':specialization,

    }
    return render(request,'admin/manage_specialization.html',context)

@admin_required
def DELETE_SPECIALIZATION(request,id):
    specialization = Specialization.objects.get(id=id)
    specialization.delete()
    messages.success(request,'Record Delete Succeesfully!!!')
    
    return redirect('manage_specilizations')

@admin_required
def UPDATE_SPECIALIZATION(request,id):
    specialization = Specialization.objects.get(id=id)
    
    context = {
         'specialization':specialization,
    }

    return render(request,'admin/update_specialization.html',context)

@admin_required
def UPDATE_SPECIALIZATION_DETAILS(request):
        if request.method == 'POST':
          sep_id = request.POST.get('sep_id')
          sname = request.POST.get('sname')
          sepcialization = Specialization.objects.get(id=sep_id) 
          sepcialization.sname = sname
          sepcialization.save()   
          messages.success(request,"Your specialization detail has been updated successfully")
          return redirect('manage_specilizations')
        return render(request, 'admin/update_specialization.html')

@admin_required
def DoctorList(request):
    doctorlist = DoctorReg.objects.all()
    context = {'doctorlist':doctorlist,

    }
    return render(request,'admin/doctor-list.html',context)

@admin_required
def ViewDoctorDetails(request,id):
    doctorlist1=DoctorReg.objects.filter(id=id)
    context={'doctorlist1':doctorlist1

    }

    return render(request,'admin/doctor-details.html',context)

@admin_required
def ViewDoctorAppointmentList(request,id):
    patientdetails=Appointment.objects.filter(doctor_id=id)
    context={'patientdetails':patientdetails

    }

    return render(request,'admin/doctor_appointment_list.html',context)

@admin_required
def ViewPatientDetails(request,id):
    patientdetails=Appointment.objects.filter(id=id)
    context={'patientdetails':patientdetails

    }

    return render(request,'admin/patient_appointment_details.html',context)

@admin_required
def Search_Doctor(request):
    if request.method == "GET":
        query = request.GET.get('query', '')
        if query:
            # Filter records where email or mobilenumber contains the query
            searchdoc = DoctorReg.objects.filter(mobilenumber__icontains=query) | DoctorReg.objects.filter(admin__first_name__icontains=query) | DoctorReg.objects.filter(admin__last_name__icontains=query)
            messages.info(request, "Search against " + query)
            return render(request, 'admin/search-doctor.html', {'searchdoc': searchdoc, 'query': query})
        else:
            messages.info(request, "No record found")
            return render(request, 'admin/search-doctor.html', {})

@admin_required
def Doctor_Between_Date_Report(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    doctor = []

    if start_date and end_date:
        # Validate the date inputs
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            return render(request, 'admin/doctor-between-date.html', {'doctor': doctor, 'error_message': 'Invalid date format'})

        # Filter visitors between the given date range
        doctor = DoctorReg.objects.filter(regdate_at__range=(start_date, end_date))

    return render(request, 'admin/doctor-between-date.html', {'doctor': doctor,'start_date':start_date,'end_date':end_date})


@admin_required
def WEBSITE_UPDATE(request):
    page = Page.objects.all()
    context = {"page":page,

    }
    return render(request,'admin/website.html',context)

@admin_required
def UPDATE_WEBSITE_DETAILS(request):
    if request.method == 'POST':
          web_id = request.POST.get('web_id')
          pagetitle = request.POST['pagetitle']
          address = request.POST['address']
          aboutus = request.POST['aboutus']
          email = request.POST['email']
          mobilenumber = normalize_phone_number(request.POST['mobilenumber'])
          page =Page.objects.get(id=web_id)
          page.pagetitle = pagetitle
          page.address = address
          page.aboutus = aboutus
          page.email = email
          page.mobilenumber = mobilenumber
          page.save()
          messages.success(request,"Your website detail has been updated successfully")
          return redirect('website_update')
    return render(request,'admin/website.html')

@admin_required
def Doctor_Specific_Report(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    doctor_id = request.GET.get('doctor_id')
    download = request.GET.get('download')
    
    appointments = []
    doctors = DoctorReg.objects.all()
    formatted_start_date = None
    formatted_end_date = None

    if start_date and end_date and doctor_id:
        try:
            # First validate the dates
            start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
            
            # Store formatted dates for display
            formatted_start_date = start_date
            formatted_end_date = end_date
            
            doctor = DoctorReg.objects.get(id=doctor_id)
            appointments = Appointment.objects.filter(
                doctor_id=doctor,
                date_of_appointment__range=(start_date_obj, end_date_obj)
            )

            if download == 'true':
                import csv
                from django.http import HttpResponse
                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = f'attachment; filename="doctor_report_{doctor.admin.first_name}_{start_date}_to_{end_date}.csv"'
                
                writer = csv.writer(response)
                writer.writerow(['Appointment ID', 'Patient Name', 'Appointment Date', 'Appointment Time', 'Status', 'Created At'])
                
                for appointment in appointments:
                    status = 'Not Updated Yet' if appointment.status == '0' else appointment.status
                    writer.writerow([
                        appointment.appointmentnumber,
                        appointment.fullname,
                        appointment.date_of_appointment,
                        appointment.time_of_appointment,
                        status,
                        appointment.created_at
                    ])
                
                return response

        except ValueError:
            return render(request, 'admin/doctor-specific-report.html', {
                'appointments': appointments,
                'doctors': doctors,
                'error_message': 'Invalid date format. Please use YYYY-MM-DD format.',
                'start_date': start_date,
                'end_date': end_date,
                'selected_doctor_id': doctor_id
            })
        except DoctorReg.DoesNotExist:
            return render(request, 'admin/doctor-specific-report.html', {
                'appointments': appointments,
                'doctors': doctors,
                'error_message': 'Doctor not found',
                'start_date': start_date,
                'end_date': end_date,
                'selected_doctor_id': doctor_id
            })

    return render(request, 'admin/doctor-specific-report.html', {
        'appointments': appointments,
        'doctors': doctors,
        'start_date': start_date,
        'end_date': end_date,
        'selected_doctor_id': doctor_id
    })
