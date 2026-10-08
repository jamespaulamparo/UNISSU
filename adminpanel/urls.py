from django.urls import path


from . import views


app_name = 'adminpanel'


urlpatterns = [
    path('login/', views.admin_login_view, name='admin_login'),
    path('students/orders/', views.student_orders, name='student_orders'),
    path('students/<int:user_id>/', views.student_order_detail, name='student_order_detail'),
    path('', views.dashboard, name='dashboard'),
    path('reports/', views.reports, name='reports'),
    path('orders/', views.orders_list, name='orders_list'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('orders/<int:order_id>/update/', views.update_order_status, name='update_order_status'),
    path('users/', views.users_list, name='users_list'),
    path('users/<int:user_id>/', views.user_detail, name='user_detail'),
    path('products/', views.products_list, name='products_list'),
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),
    path('products/update-size-stock/<int:size_id>/', views.update_size_stock, name='update_size_stock'),
]
