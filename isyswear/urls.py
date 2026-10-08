from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static
from .views import home
from users import views as user_views

urlpatterns = [
    # Institutional Storefront Catalog
    path('', home, name='home'),
    path('home/', home),

    # Unified Authentication Routes
    path('login/', user_views.login_view, name='login'),
    path('register/', user_views.register, name='register'),
    path('logout/', user_views.logout_view, name='logout'),

    # Modular System Apps
    path('users/', include('users.urls')),
    path('products/', include('products.urls')),
    path('cart/', include('cart.urls')),
    path('orders/', include('orders.urls', namespace='orders')),

    # Administrative Portals
    path('admin/', admin.site.urls),
    path('panel/', include('adminpanel.urls')),
    path('adminpanel/', lambda request: redirect('/panel/', permanent=False)),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
