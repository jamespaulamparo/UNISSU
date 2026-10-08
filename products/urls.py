from django.urls import path
from . import views

urlpatterns = [
    path('', views.uniforms, name='products_index'),
    path('uniforms/', views.uniforms, name='uniforms'),
    path('uniforms/<int:pk>/', views.uniform_detail, name='uniform_detail'),
]
