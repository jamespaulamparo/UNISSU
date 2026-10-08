from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    ROLE_STUDENT = 'student'
    ROLE_ADMIN = 'admin'
    ROLE_STAFF = 'staff'
    ROLE_CHOICES = [
        (ROLE_STUDENT, 'Student'),
        (ROLE_ADMIN, 'Administrator'),
        (ROLE_STAFF, 'Staff / Faculty'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_STUDENT)
    student_id = models.CharField(max_length=30, blank=True, null=True, verbose_name="Student / ID Number")
    full_name = models.CharField(max_length=150, blank=True, null=True, verbose_name="Full Name")
    course_year = models.CharField(max_length=100, blank=True, null=True, verbose_name="Program & Year Level")
    phone_number = models.CharField(max_length=20, blank=True, null=True, verbose_name="Contact Number")
    address = models.TextField(blank=True, null=True, verbose_name="Complete Address")
    assigned_products = models.ManyToManyField('products.Uniform', blank=True, related_name='assigned_students')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        role_label = dict(self.ROLE_CHOICES).get(self.role, self.role)
        display = self.full_name or self.user.get_full_name() or self.user.username
        return f"{display} ({role_label})"

    @property
    def is_admin(self):
        return self.user.is_staff or self.user.is_superuser or self.role in [self.ROLE_ADMIN, self.ROLE_STAFF]

    @property
    def display_name(self):
        return self.full_name or self.user.get_full_name() or self.user.username


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Ensure every User always has an associated Profile.
    Automatically assigns admin role if user has staff/superuser flag.
    """
    if created:
        role = Profile.ROLE_ADMIN if (instance.is_staff or instance.is_superuser) else Profile.ROLE_STUDENT
        Profile.objects.create(
            user=instance,
            role=role,
            full_name=instance.get_full_name() or instance.username
        )
    else:
        # If user flags changed, sync role if appropriate
        profile = getattr(instance, 'profile', None)
        if profile is None:
            role = Profile.ROLE_ADMIN if (instance.is_staff or instance.is_superuser) else Profile.ROLE_STUDENT
            Profile.objects.create(user=instance, role=role)
        elif (instance.is_staff or instance.is_superuser) and profile.role == Profile.ROLE_STUDENT:
            profile.role = Profile.ROLE_ADMIN
            profile.save(update_fields=['role'])
