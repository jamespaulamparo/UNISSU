from django.urls import path
from .views import create_order, list_orders, update_order, delete_order, order_confirmation, order_details, order_history, order_receipt

app_name = 'orders'

urlpatterns = [
    path('create/', create_order, name='create_order'),
    path('list/', list_orders, name='list_orders'),
    path('update/<int:order_id>/', update_order, name='update_order'),
    path('delete/<int:order_id>/', delete_order, name='delete_order'),
    path('confirmation/', order_confirmation, name='order_confirmation'),
    path('details/<int:order_id>/', order_details, name='order_details'),
    path('history/', order_history, name='order_history'),
    path('receipt/<int:order_id>/', order_receipt, name='order_receipt'),
]
