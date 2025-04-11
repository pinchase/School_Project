from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomUser

def BASE(request):
    return render(request, 'base.html')

def LOGIN(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            if user.user_type == '1':
                return redirect('admin_home')
            elif user.user_type == '2':
                return redirect('doctor_home')
            else:
                return redirect('index')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')
    return render(request, 'login.html')

def doLogout(request):
    logout(request)
    return redirect('login')

@login_required
def PROFILE(request):
    return render(request, 'profile.html')

@login_required
def PROFILE_UPDATE(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        
        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.username = username
        user.save()
        
        messages.success(request, 'Profile updated successfully')
        return redirect('profile')
    return render(request, 'profile.html')

@login_required
def CHANGE_PASSWORD(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        user = request.user
        if user.check_password(current_password):
            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password changed successfully')
                return redirect('login')
            else:
                messages.error(request, 'New passwords do not match')
        else:
            messages.error(request, 'Current password is incorrect')
    return render(request, 'change_password.html')
