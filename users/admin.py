from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.db.models import Count
from .models import Profile
from orders.models import Order

User = get_user_model()

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'

class CustomUserAdmin(BaseUserAdmin):
    inlines = [ProfileInline]
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined', 'orders_count', 'assigned_count']
    list_filter = BaseUserAdmin.list_filter
    search_fields = BaseUserAdmin.search_fields + ('first_name', 'last_name')
    
    def orders_count(self, obj):
        return obj.orders.count()
    orders_count.short_description = 'Orders Count'
    
    def assigned_count(self, obj):
        profile = getattr(obj, 'profile', None)
        return profile.assigned_products.count() if profile else 0
    assigned_count.short_description = 'Assigned Products Count'

    def get_queryset(self, request):
        qs = super().get_queryset(request).annotate(
            orders_count=Count('orders'),
            assigned_count=Count('profile__assigned_products', distinct=True)
        )
        return qs

# Unregister default and register custom
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

admin.site.register(User, CustomUserAdmin)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'phone_number', 'assigned_products_count')
    
    def assigned_products_count(self, obj):
        return obj.assigned_products.count()
    assigned_products_count.short_description = 'Assigned Products'

