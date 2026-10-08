from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('login-register/', views.login_view, name='login_register'),  # Legacy alias
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.profile, name='profile_edit'),
    path('change-password/', views.change_password, name='change_password'),
    path('password-reset/', views.password_reset, name='password_reset'),
    path('password-reset/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
    path('delete-account/', views.delete_account, name='delete_account'),
]
