from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponseForbidden

from .forms import (
    LoginForm,
    RegistrationForm,
    ProfileForm,
    ChangePasswordForm,
    PasswordResetForm,
    PasswordResetConfirmForm
)
from .models import Profile


def _authenticate_user(request, identifier, password):
    """
    Authenticate against username, email address, or student ID.
    Gracefully trims input and handles case-insensitivity.
    """
    if not identifier or not password:
        return None
    identifier = str(identifier).strip()

    # 1. Direct standard username authentication
    user = authenticate(request, username=identifier, password=password)
    if user is not None:
        return user

    # 2. Email match
    if '@' in identifier:
        user_by_email = User.objects.filter(email__iexact=identifier).first()
        if user_by_email:
            user = authenticate(request, username=user_by_email.username, password=password)
            if user is not None:
                return user

    # 3. Case-insensitive username match
    user_by_name = User.objects.filter(username__iexact=identifier).first()
    if user_by_name:
        user = authenticate(request, username=user_by_name.username, password=password)
        if user is not None:
            return user

    # 4. Institutional Student ID lookup via Profile
    profile_by_id = Profile.objects.filter(student_id__iexact=identifier).select_related('user').first()
    if profile_by_id and profile_by_id.user:
        user = authenticate(request, username=profile_by_id.user.username, password=password)
        if user is not None:
            return user

    return None


def _get_post_login_redirect(request, user):
    """
    Smart institutional post-login routing:
    - If a valid next URL is provided, redirect to it.
    - If user is Staff / Superuser / Admin role, redirect to /panel/ (adminpanel dashboard).
    - Otherwise redirect to university store catalog ('home').
    """
    next_url = request.POST.get('next') or request.GET.get('next')
    if next_url and next_url.startswith('/') and not next_url.startswith('//'):
        excluded = ['/login/', '/register/', '/logout/', '/panel/login/']
        if not any(next_url.startswith(ex) for ex in excluded):
            return redirect(next_url)

    is_admin = user.is_staff or user.is_superuser or (
        hasattr(user, 'profile') and user.profile.is_admin
    )
    if is_admin:
        return redirect('adminpanel:dashboard')
    return redirect('home')


def login_view(request):
    """Unified portal login for both students and university administrators."""
    if request.user.is_authenticated:
        return _get_post_login_redirect(request, request.user)

    next_url = request.POST.get('next') or request.GET.get('next') or ''
    login_form = LoginForm(request.POST or None)
    register_form = RegistrationForm()

    if request.method == 'POST':
        if login_form.is_valid():
            identifier = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            remember_me = login_form.cleaned_data.get('remember_me', False)

            user = _authenticate_user(request, identifier, password)
            if user is not None:
                if not user.is_active:
                    login_form.add_error(None, "This account is inactive. Please contact the campus administrator.")
                else:
                    login(request, user)
                    if not remember_me:
                        request.session.set_expiry(0)  # expires on browser close
                    display_name = getattr(user, 'profile', None) and user.profile.display_name or user.username
                    messages.success(request, f"Welcome to UNISSU, {display_name}!")
                    return _get_post_login_redirect(request, user)
            else:
                login_form.add_error(None, "Invalid credentials. Please verify your Student ID, username, or password.")

    return render(request, 'pages/loginAndregister.html', {
        'login_form': login_form,
        'register_form': register_form,
        'active_tab': 'login',
        'next': next_url,
    })


def register(request):
    """Institutional student registration flow."""
    if request.user.is_authenticated:
        return _get_post_login_redirect(request, request.user)

    next_url = request.POST.get('next') or request.GET.get('next') or ''
    login_form = LoginForm()
    register_form = RegistrationForm(request.POST or None)

    if request.method == 'POST':
        if register_form.is_valid():
            user = register_form.save()
            # Explicit backend login ensures session validity
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            display_name = getattr(user, 'profile', None) and user.profile.display_name or user.username
            messages.success(request, f"Account created successfully! Welcome to UNISSU, {display_name}.")
            return _get_post_login_redirect(request, user)
        else:
            messages.error(request, "Please resolve the highlighted validation issues to create your account.")

    return render(request, 'pages/loginAndregister.html', {
        'login_form': login_form,
        'register_form': register_form,
        'active_tab': 'register',
        'next': next_url,
    })


def logout_view(request):
    """Secure logout view with feedback."""
    logout(request)
    messages.info(request, "You have been signed out of your UNISSU session.")
    return redirect('login')


@login_required
def profile(request):
    """Student profile viewing and management."""
    user_profile = getattr(request.user, 'profile', None)
    if user_profile is None:
        user_profile = Profile.objects.create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user_profile.full_name = data.get('full_name')
            user_profile.student_id = data.get('student_id')
            user_profile.course_year = data.get('course_year')
            user_profile.phone_number = data.get('phone_number')
            user_profile.address = data.get('address')
            user_profile.save()

            new_email = data.get('email')
            if new_email and new_email != request.user.email:
                if User.objects.filter(email__iexact=new_email).exclude(pk=request.user.pk).exists():
                    messages.error(request, "That email address is already taken by another account.")
                    return redirect('profile')
                request.user.email = new_email
                request.user.save()

            messages.success(request, "Your student profile has been updated successfully.")
            return redirect('profile')
        else:
            messages.error(request, "Please fix the errors in the profile form.")
    else:
        initial = {
            'full_name': user_profile.full_name or request.user.get_full_name(),
            'student_id': user_profile.student_id,
            'course_year': user_profile.course_year,
            'phone_number': user_profile.phone_number,
            'address': user_profile.address,
            'email': request.user.email,
        }
        form = ProfileForm(initial=initial)

    total_spent = sum(order.total_amount for order in request.user.orders.all()) if hasattr(request.user, 'orders') else 0
    completed_orders = request.user.orders.filter(status='delivered').count() if hasattr(request.user, 'orders') else 0

    return render(request, 'pages/profile.html', {
        'profile_form': form,
        'profile': user_profile,
        'total_spent': total_spent,
        'completed_orders': completed_orders,
    })


@login_required
def change_password(request):
    """Change password for authenticated student/admin."""
    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Keep session active
            messages.success(request, 'Your password was changed successfully.')
            return redirect('profile')
    else:
        form = ChangePasswordForm(request.user)
    return render(request, 'pages/changePassword.html', {'form': form})


def password_reset(request):
    """Initiate self-service password reset."""
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.filter(email__iexact=email).first()
            if user:
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                reset_url = request.build_absolute_uri(
                    reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
                )
                send_mail(
                    'UNISSU - Password Reset Instructions',
                    f'Hello {user.username},\n\nClick the link below to reset your password:\n{reset_url}\n\nThis security link expires in 1 hour.',
                    'noreply@dmmmsu.edu.ph',
                    [email],
                    fail_silently=True,
                )
            # Uniform message for security to prevent user enumeration
            messages.info(request, "If that email is registered in our portal, a password reset link has been dispatched.")
            return redirect('login')
    else:
        form = PasswordResetForm()
    return render(request, 'pages/passwordReset.html', {'form': form})


def password_reset_confirm(request, uidb64, token):
    """Confirm and set new password from reset link."""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        messages.error(request, 'The password reset link is invalid or malformed.')
        return redirect('login')

    if not default_token_generator.check_token(user, token):
        messages.error(request, 'This password reset link has expired.')
        return redirect('login')

    if request.method == 'POST':
        form = PasswordResetConfirmForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your password has been successfully reset. You can now sign in.')
            return redirect('login')
    else:
        form = PasswordResetConfirmForm(user)

    return render(request, 'pages/passwordResetConfirm.html', {'form': form, 'uid': uidb64, 'token': token})


@login_required
def delete_confirm(request):
    """Account deletion with confirmation."""
    if request.method == 'POST':
        confirm_text = request.POST.get('confirm_text', '').strip().upper()
        if confirm_text == 'DELETE MY ACCOUNT':
            user = request.user
            logout(request)
            user.delete()
            messages.success(request, "Your account and data have been removed from UNISSU.")
            return redirect('home')
        else:
            messages.error(request, "Confirmation text did not match. Account was not deleted.")
            return redirect('profile')

    return render(request, 'pages/delete_confirm.html', {'user': request.user})


def delete_account(request):
    return delete_confirm(request)
