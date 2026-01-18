from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings

import random
import string

from .forms import (
    StudentRegistrationForm,
    PasswordResetRequestForm,
    OTPPasswordResetForm,
)
from allotment.models import Student


# -------------------------
# Student Registration
# -------------------------
def student_register(request):
    """
    Handles new student user + Student profile creation.
    Only for normal students, not admins.
    """
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            return redirect('admin_dashboard')
        return redirect('student_dashboard')

    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
            except Exception:
                form.add_error('email', 'This email or roll number might already be registered.')
            else:
                login(request, user)
                messages.success(request, "Registration successful. Welcome to SmartAllot!")
                return redirect('student_dashboard')
    else:
        form = StudentRegistrationForm()

    return render(request, 'core/student_register.html', {'form': form})


# -------------------------
# Student Login
# -------------------------
def student_login(request):
    """
    Login view for students (non-staff users).
    """
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            return redirect('admin_dashboard')
        return redirect('student_dashboard')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()

            # Prevent staff/admin login here
            if user.is_staff or user.is_superuser:
                messages.error(request, "Please use the admin login page.")
                return redirect('admin_login')

            login(request, user)
            return redirect('student_dashboard')
    else:
        form = AuthenticationForm()

    return render(request, 'core/student_login.html', {'form': form})


# -------------------------
# Admin Login
# -------------------------
def admin_login(request):
    """
    Login view for admins (staff/superuser).
    """
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            return redirect('admin_dashboard')
        return redirect('student_dashboard')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()

            if not (user.is_staff or user.is_superuser):
                messages.error(request, "You are not authorized as admin.")
            else:
                login(request, user)
                return redirect('admin_dashboard')
    else:
        form = AuthenticationForm()

    return render(request, 'core/admin_login.html', {'form': form})


# -------------------------
# Logout
# -------------------------
def logout_view(request):
    """
    Logs the user out and redirects to the home page (allotment.home).
    """
    logout(request)
    return redirect('home')  # 'home' is defined in allotment/urls.py → allotment.views.home


# -------------------------
# Password Reset with OTP (Email)
# -------------------------
def _generate_otp(length=6):
    return ''.join(random.choices(string.digits, k=length))


def forgot_password(request):
    """
    Step 1: User enters email, we send OTP and store it in session.
    """
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                form.add_error('email', 'No account found with this email.')
            else:
                otp = _generate_otp()
                # Store details in session
                request.session['password_reset_user_id'] = user.id
                request.session['password_reset_otp'] = otp
                request.session['password_reset_time'] = timezone.now().isoformat()

                subject = "SmartAllot Password Reset OTP"
                message = f"Your OTP for password reset is: {otp}\nThis code is valid for a short time."
                from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', None)

                try:
                    send_mail(subject, message, from_email, [email])
                    messages.success(request, "OTP has been sent to your email.")
                    return redirect('reset_password_with_otp')
                except Exception as e:
                    form.add_error(None, f"Error sending email: {e}")
    else:
        form = PasswordResetRequestForm()

    return render(request, 'core/forgot_password.html', {'form': form})


def reset_password_with_otp(request):
    """
    Step 2: User enters OTP + new password.
    """
    user_id = request.session.get('password_reset_user_id')
    session_otp = request.session.get('password_reset_otp')

    if not user_id or not session_otp:
        messages.error(request, "Password reset session expired. Please request a new OTP.")
        return redirect('forgot_password')

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, "User not found. Please request a new OTP.")
        return redirect('forgot_password')

    if request.method == 'POST':
        form = OTPPasswordResetForm(request.POST)
        if form.is_valid():
            otp_entered = form.cleaned_data['otp']
            if otp_entered != session_otp:
                form.add_error('otp', 'Invalid OTP.')
            else:
                new_password = form.cleaned_data['new_password1']
                user.set_password(new_password)
                user.save()

                # Clear session
                for key in ['password_reset_user_id', 'password_reset_otp', 'password_reset_time']:
                    if key in request.session:
                        del request.session[key]

                messages.success(request, "Password successfully reset. You can now log in.")
                return redirect('student_login')
    else:
        form = OTPPasswordResetForm()

    return render(request, 'core/reset_password_with_otp.html', {'form': form})
