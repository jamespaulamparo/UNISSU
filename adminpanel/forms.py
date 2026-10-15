from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import transaction
from users.models import Profile


class AdminUserCreationForm(forms.Form):
    """
    Form for authorized administrators/superusers to create new staff or administrator accounts.
    Strictly isolated to authenticated admin panel sessions.
    """
    ROLE_CHOICES_STAFF = [
        ('staff', 'Staff / Faculty Personnel'),
        ('admin', 'Store Administrator'),
    ]
    ROLE_CHOICES_SUPERUSER = [
        ('staff', 'Staff / Faculty Personnel'),
        ('admin', 'Store Administrator'),
        ('superuser', 'System Superuser (Full Privileges)'),
    ]

    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g. supply_staff01'
        })
    )
    full_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g. Maria Santos'
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g. msantos@dmmmsu.edu.ph'
        })
    )
    role = forms.ChoiceField(
        choices=ROLE_CHOICES_STAFF,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Temporary or permanent password'
        }),
        min_length=6
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm password'
        })
    )

    def __init__(self, *args, is_superuser=False, **kwargs):
        super().__init__(*args, **kwargs)
        if is_superuser:
            self.fields['role'].choices = self.ROLE_CHOICES_SUPERUSER

    def clean_username(self):
        username = self.cleaned_data.get('username', '').strip()
        if User.objects.filter(username__iexact=username).exists():
            raise ValidationError("A user with this username already exists.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("A user with this email address already exists.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password')
        p2 = cleaned_data.get('password_confirm')
        if p1 and p2 and p1 != p2:
            self.add_error('password_confirm', "Passwords do not match.")
        return cleaned_data

    @transaction.atomic
    def save(self):
        data = self.cleaned_data
        role = data['role']
        is_su = (role == 'superuser')

        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password']
        )
        user.is_staff = True
        user.is_superuser = is_su
        
        name_parts = data['full_name'].strip().split(' ', 1)
        user.first_name = name_parts[0]
        user.last_name = name_parts[1] if len(name_parts) > 1 else ''
        user.save()

        profile, _ = Profile.objects.get_or_create(user=user)
        profile.full_name = data['full_name']
        profile.role = Profile.ROLE_ADMIN if (is_su or role == 'admin') else Profile.ROLE_STAFF
        profile.save()

        return user
