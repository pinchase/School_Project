from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import CustomUser, DoctorReg, Specialization, Appointment, Page

@login_required
def ADMINHOME(request):
    return render(request, 'admin/adminhome.html')

@login_required
def SPECIALIZATION(request):
    if request.method == 'POST':
        sname = request.POST.get('sname')
        Specialization.objects.create(sname=sname)
        return redirect('manage_specilizations')
    return render(request, 'admin/specialization.html')

@login_required
def MANAGESPECIALIZATION(request):
    specializations = Specialization.objects.all()
    return render(request, 'admin/managespecialization.html', {'specializations': specializations})

@login_required
def DELETE_SPECIALIZATION(request, id):
    specialization = Specialization.objects.get(id=id)
    specialization.delete()
    return redirect('manage_specilizations')

@login_required
def UPDATE_SPECIALIZATION(request, id):
    specialization = Specialization.objects.get(id=id)
    return render(request, 'admin/updatespecialization.html', {'specialization': specialization})

@login_required
def UPDATE_SPECIALIZATION_DETAILS(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        sname = request.POST.get('sname')
        specialization = Specialization.objects.get(id=id)
        specialization.sname = sname
        specialization.save()
        return redirect('manage_specilizations')
    return redirect('manage_specilizations')

@login_required
def DoctorList(request):
    doctors = DoctorReg.objects.all()
    return render(request, 'admin/doctorlist.html', {'doctors': doctors})

@login_required
def ViewDoctorDetails(request, id):
    doctor = DoctorReg.objects.get(id=id)
    return render(request, 'admin/viewdoctordetails.html', {'doctor': doctor})

@login_required
def ViewDoctorAppointmentList(request, id):
    doctor = DoctorReg.objects.get(id=id)
    appointments = Appointment.objects.filter(doctor_id=doctor)
    return render(request, 'admin/viewdoctorappointmentlist.html', {'appointments': appointments})

@login_required
def ViewPatientDetails(request, id):
    appointment = Appointment.objects.get(id=id)
    return render(request, 'admin/viewpatientdetails.html', {'appointment': appointment})

@login_required
def Search_Doctor(request):
    if request.method == 'POST':
        search_query = request.POST.get('search')
        doctors = DoctorReg.objects.filter(admin__first_name__icontains=search_query) | \
                 DoctorReg.objects.filter(admin__last_name__icontains=search_query)
        return render(request, 'admin/doctorlist.html', {'doctors': doctors})
    return redirect('viewdoctorlist')

@login_required
def Doctor_Between_Date_Report(request):
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        appointments = Appointment.objects.filter(date_of_appointment__range=[start_date, end_date])
        return render(request, 'admin/doctorreport.html', {'appointments': appointments})
    return render(request, 'admin/doctorreport.html')

@login_required
def WEBSITE_UPDATE(request):
    page = Page.objects.first()
    return render(request, 'admin/websiteupdate.html', {'page': page})

@login_required
def UPDATE_WEBSITE_DETAILS(request):
    if request.method == 'POST':
        page = Page.objects.first()
        if not page:
            page = Page()
        page.pagetitle = request.POST.get('pagetitle')
        page.address = request.POST.get('address')
        page.aboutus = request.POST.get('aboutus')
        page.email = request.POST.get('email')
        page.mobilenumber = request.POST.get('mobilenumber')
        page.save()
        return redirect('website_update')
    return redirect('website_update') 