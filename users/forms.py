from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.core.exceptions import ValidationError
from django.db import transaction
from .models import Profile


class LoginForm(forms.Form):
    """Clean, institutional login form supporting username, email, or student ID."""
    username = forms.CharField(
        label="Student ID, Username, or Institutional Email",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your student ID, username, or email',
            'autocomplete': 'username',
            'autofocus': True,
        }),
        required=True
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password',
            'autocomplete': 'current-password',
        }),
        required=True
    )
    remember_me = forms.BooleanField(
        label="Keep me signed in on this computer",
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-checkbox'})
    )


class RegistrationForm(forms.ModelForm):
    """Student and user onboarding form with institutional validation."""
    full_name = forms.CharField(
        max_length=150,
        required=True,
        label="Full Name",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g. Juan C. Dela Cruz'
        })
    )
    student_id = forms.CharField(
        max_length=30,
        required=False,
        label="Student / ID Number",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g. 12x-xxxx-x'
        })
    )
    course_year = forms.CharField(
        max_length=100,
        required=False,
        label="Program & Year Level",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g. BSIS 3B'
        })
    )
    email = forms.EmailField(
        required=True,
        label="Email Address",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g. jdelacruz@dmmmsu.edu.ph'
        })
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Create a password',
            'autocomplete': 'new-password'
        }),
        help_text="Password must be at least 6 characters long."
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Re-enter your password',
            'autocomplete': 'new-password'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'email')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. jdelacruz'
            })
        }

    def clean_username(self):
        username = self.cleaned_data.get('username', '').strip()
        if not username:
            raise ValidationError("Please provide a valid username.")
        if len(username) < 3:
            raise ValidationError("Username must be at least 3 characters long.")
        if User.objects.filter(username__iexact=username).exists():
            raise ValidationError("An account with this username already exists.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip().lower()
        if not email:
            raise ValidationError("A valid email address is required.")
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("An account with this email address already exists.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2:
            if len(password1) < 6:
                self.add_error('password1', "Password must be at least 6 characters long.")
            if password1 != password2:
                self.add_error('password2', "Passwords do not match. Please verify and re-enter.")
        return cleaned_data

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.email = self.cleaned_data['email']
        
        # Populate first_name / last_name from full_name if possible
        full_name = self.cleaned_data.get('full_name', '').strip()
        name_parts = full_name.split(' ', 1)
        user.first_name = name_parts[0]
        user.last_name = name_parts[1] if len(name_parts) > 1 else ''

        if commit:
            user.save()
            profile = getattr(user, 'profile', None)
            if profile is None:
                profile = Profile.objects.create(user=user)
            profile.full_name = full_name
            profile.student_id = self.cleaned_data.get('student_id', '').strip()
            profile.course_year = self.cleaned_data.get('course_year', '').strip()
            profile.role = Profile.ROLE_STUDENT
            profile.save()
        return user


class ProfileForm(forms.Form):
    full_name = forms.CharField(
        max_length=150,
        required=True,
        label='Full Name',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        required=True,
        label='Email Address',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    student_id = forms.CharField(
        max_length=30,
        required=False,
        label='Student / ID Number',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    course_year = forms.CharField(
        max_length=100,
        required=False,
        label='Program & Year Level',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    phone_number = forms.CharField(
        max_length=20,
        required=False,
        label='Contact Number',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    address = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        required=False,
        label='Delivery / Campus Address'
    )


class ChangePasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class PasswordResetForm(forms.Form):
    email = forms.EmailField(
        required=True,
        label='Institutional / Registered Email',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'name@dmmmsu.edu.ph'})
    )


class PasswordResetConfirmForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
