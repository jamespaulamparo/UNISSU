import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Verification'),
        ('approved', 'Approved / Ready for Pickup'),
        ('completed', 'Completed / Claimed'),
        ('rejected', 'Rejected'),
        ('processing', 'Processing (Legacy)'),
        ('shipped', 'Order Arrived (Legacy)'),
        ('cancelled', 'Cancelled'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash on Pickup / Reservation'),
        ('online', 'Online Payment (Reference Upload)'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', null=True, blank=True)
    customer_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    student_id = models.CharField(max_length=50, blank=True, null=True)
    course_year = models.CharField(max_length=100, blank=True, null=True)
    
    # Counter Pickup Only — No Deliveries
    pickup_location = models.CharField(
        max_length=255,
        default='DMMMSU NLUC CIS Faculty Office',
        blank=True
    )
    address = models.TextField(blank=True, default='Counter Pickup')
    
    # Payment verification details
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default='cash'
    )
    payment_reference = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Payment Reference / Transaction No."
    )
    payment_receipt = models.ImageField(
        upload_to='receipts/',
        blank=True,
        null=True,
        verbose_name="Payment Receipt Screenshot"
    )

    # Order lifecycle & Claim Slip
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='pending')
    claim_code = models.CharField(max_length=64, blank=True, null=True, unique=True)
    admin_notes = models.TextField(blank=True, null=True, verbose_name="Staff / Admin Notes")
    
    verified_at = models.DateTimeField(blank=True, null=True)
    claimed_at = models.DateTimeField(blank=True, null=True)
    order_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.claim_code:
            self.claim_code = f"CLM-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Order {self.id} ({self.claim_code}) - {self.customer_name}'
    
    @property
    def get_total(self):
        total = sum(item.get_total_price() for item in self.items.all())
        return total if total > 0 else self.total_amount

    @property
    def is_ready_for_pickup(self):
        return self.status == 'approved'

    @property
    def is_completed(self):
        return self.status == 'completed'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product_id = models.IntegerField()
    product_name = models.CharField(max_length=255)
    size = models.CharField(max_length=50, blank=True, default='')
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        size_str = f" ({self.size})" if self.size else ""
        return f'{self.product_name}{size_str} x {self.quantity}'
    
    def get_total_price(self):
        return self.price * self.quantity
