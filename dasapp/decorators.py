from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from .models import CustomUser


def role_required(*allowed_roles):
    def decorator(view_func):
        @login_required(login_url='/')
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.user_type in allowed_roles:
                return view_func(request, *args, **kwargs)
            messages.error(request, 'You do not have permission to access that page.')
            if request.user.user_type == CustomUser.UserType.DOCTOR:
                return redirect('doctor_home')
            return redirect('index')

        return _wrapped_view

    return decorator


admin_required = role_required(CustomUser.UserType.ADMIN)
doctor_required = role_required(CustomUser.UserType.DOCTOR)
