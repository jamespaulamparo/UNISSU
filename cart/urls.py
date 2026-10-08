from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart_view, name='cart'),
    path('cart/', views.cart_view),  # Alias for backward compatibility
    path('checkout/', views.checkout, name='checkout'),
    path('add/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('cart/add/<int:pk>/', views.add_to_cart),  # Alias
    path('remove/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/remove/<int:pk>/', views.remove_from_cart),  # Alias
]
