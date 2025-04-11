from django.shortcuts import render,redirect,HttpResponse
from dasapp.EmailBackEnd import EmailBackEnd
from django.contrib.auth import  logout,login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from dasapp.models import CustomUser
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from dasapp.models import DoctorReg
User = get_user_model()
def BASE(request):
    return render(request,'base.html')


def LOGIN(request):
    return render(request,'login.html')

def doLogout(request):
    logout(request)
    return redirect('login')

def doLogin(request):
    if request.method == 'POST':
        user = EmailBackEnd.authenticate(request,
                                         username=request.POST.get('email'),
                                         password=request.POST.get('password')
                                         )
        if user!=None:
            login(request,user)
            user_type = user.user_type
            if user_type == '1':
                 return redirect('admin_home')
            elif user_type == '2':
                 return redirect('doctor_home')
            elif user_type == '3':
                return HttpResponse("This is User panel")
            
            
        else:
                messages.error(request,'Email or Password is not valid')
                return redirect('login')
    else:
            messages.error(request,'Email or Password is not valid')
            return redirect('login')


login_required(login_url='/')
def PROFILE(request):
    user = CustomUser.objects.get(id = request.user.id)
    context = {
        "user":user,
    }
    return render(request,'profile.html',context)
@login_required(login_url = '/')
def PROFILE_UPDATE(request):
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        print(profile_pic)
        

        try:
            customuser = CustomUser.objects.get(id = request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            

            
            if profile_pic !=None and profile_pic != "":
               customuser.profile_pic = profile_pic
            customuser.save()
            messages.success(request,"Your profile has been updated successfully")
            return redirect('profile')

        except:
            messages.error(request,"Your profile updation has been failed")
    return render(request, 'profile.html')


def CHANGE_PASSWORD(request):
     context ={}
     ch = User.objects.filter(id = request.user.id)
     
     if len(ch)>0:
            data = User.objects.get(id = request.user.id)
            context["data"]:data            
     if request.method == "POST":        
        current = request.POST["cpwd"]
        new_pas = request.POST['npwd']
        user = User.objects.get(id = request.user.id)
        un = user.username
        check = user.check_password(current)
        if check == True:
          user.set_password(new_pas)
          user.save()
          messages.success(request,'Password Change  Succeesfully!!!')
          user = User.objects.get(username=un)
          login(request,user)
        else:
          messages.success(request,'Current Password wrong!!!')
          return redirect("change_password")
     return render(request,'change-password.html')

class CustomPasswordResetView(PasswordResetView):
    def form_valid(self, form):
        email = form.cleaned_data['email']
        new_password1 = self.request.POST.get('new_password1')
        new_password2 = self.request.POST.get('new_password2')
        
        try:
            # First check if the email exists in DoctorReg
            doctor = DoctorReg.objects.get(admin__email=email)
            user = doctor.admin  # Get the associated CustomUser
            
            if new_password1 and new_password2 and new_password1 == new_password2:
                # Update the password
                user.set_password(new_password1)
                user.save()
                
                messages.success(self.request, 'Password has been reset successfully. Please login with your new password.')
                return redirect('login')
            else:
                messages.error(self.request, 'Passwords do not match.')
                return redirect('password_reset')
        except DoctorReg.DoesNotExist:
            messages.error(self.request, 'No doctor found with this email address.')
            return redirect('password_reset')
        except Exception as e:
            messages.error(self.request, f'An error occurred: {str(e)}')
            return redirect('password_reset')

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid form submission. Please check your input.')
        return redirect('password_reset')

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True})
        return response

    def form_invalid(self, form):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'error': 'Passwords do not match or are invalid'})
        return super().form_invalid(form)