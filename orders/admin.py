
from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product_id', 'product_name', 'price', 'quantity')
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_add_permission(self, request, obj):
        return False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'email', 'total_amount', 'status', 'order_date')
    list_filter = ('status', 'order_date')
    search_fields = ('customer_name', 'email', 'address')
    readonly_fields = ('order_date', 'updated_at')
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product_name', 'quantity', 'price')
    search_fields = ('product_name', 'order__customer_name')
