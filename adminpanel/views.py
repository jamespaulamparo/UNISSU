from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Sum
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect


from products.models import Uniform
from orders.models import Order
from django.db.models import Count
from users.models import Profile


def _is_admin(user):
    if not user.is_authenticated:
        return False
    if user.is_staff or user.is_superuser:
        return True
    profile = getattr(user, 'profile', None)
    return profile is not None and getattr(profile, 'is_admin', False)




def admin_required(view_func):
    return login_required(user_passes_test(_is_admin)(view_func))




def _safe_int(value, default=0):
    try:
        return int(value)
    except Exception:
        return default




@admin_required
def dashboard(request):
    # Users KPIs (real)
    users_total = User.objects.count()
    staff_total = User.objects.filter(is_staff=True).count()


    # Products KPIs (real)
    products_total = Uniform.objects.count()
    total_stock = Uniform.objects.aggregate(total=Sum("stock")).get("total") or 0


    # Orders KPIs (now using real Order model)
    orders_total = Order.objects.count()
    revenue_total = Order.objects.aggregate(total=Sum("total_amount")).get("total") or 0
   
    # Latest orders
    latest_orders = Order.objects.all().order_by("-order_date")[:5]


    context = {
        "kpis": {
            "users_total": users_total,
            "staff_total": staff_total,
            "products_total": products_total,
            "total_stock": total_stock,
            "orders_total": orders_total,
            "revenue_total": revenue_total,
        },
        "latest_orders": latest_orders,
        "total_users": users_total,
        "total_orders": orders_total,
        "total_revenue": revenue_total or 0,
    }
    return render(request, "adminpanel/dashboard.html", context)


@admin_required
def reports(request):
    from django.contrib.auth.models import User
    from products.models import Uniform
    from orders.models import Order
    from django.utils import timezone
    from datetime import timedelta
   
    total_users = User.objects.count()
    total_orders = Order.objects.count()
    total_revenue = Order.objects.aggregate(total=Sum('total_amount'))['total'] or 0
    avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
   
    # Top products by sold
    top_products = Uniform.objects.order_by('-stock')[:5]
   
    # Recent activity (simplified - orders as activity)
    recent_activity = [{
        'user': order.user if hasattr(order, 'user') else User.objects.first(),
        'action': f'Order #{order.id} {"completed" if order.status == "delivered" else order.status}',
        'timestamp': order.order_date
    } for order in Order.objects.order_by('-order_date')[:10]]
   
    context = {
        'total_users': total_users,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'avg_order_value': avg_order_value,
        'top_products': top_products,
        'recent_activity': recent_activity,
    }
    return render(request, 'adminpanel/reports.html', context)




@admin_required
def users_list(request):
    qs = User.objects.annotate(
        orders_count=Count('orders'),
        assigned_count=Count('profile__assigned_products', distinct=True)
    ).prefetch_related('orders', 'profile').order_by("-date_joined")


    unused_users = User.objects.filter(
        is_superuser=False,
        is_staff=False,
        is_active=True
    ).annotate(
        orders_count=Count('orders'),
        assigned_count=Count('profile__assigned_products', distinct=True)
    ).filter(
        orders_count=0,
        assigned_count=0
    )


    unused_count = unused_users.count()


    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'cleanup_unused':
            confirm = request.POST.get('confirm')
            if confirm == 'yes':
                deleted_count, _ = unused_users.delete()
                messages.success(request, f'Successfully deleted {deleted_count} unused user(s).')
            else:
                messages.warning(request, 'Cleanup cancelled.')
            return redirect('adminpanel:users_list')


    return render(request, "adminpanel/users.html", {
        "users": qs,
        "unused_count": unused_count,
        "unused_users": unused_users  # for template row marking
    })




@admin_required
def user_detail(request, user_id: int):
    user = get_object_or_404(User, id=user_id)
    profile = getattr(user, "profile", None)
   
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'toggle_staff' and not user.is_superuser:
            user.is_staff = not user.is_staff
            user.save()
            messages.success(request, f'User staff status toggled to { "enabled" if user.is_staff else "disabled" }')
        elif action == 'toggle_active':
            user.is_active = not user.is_active
            user.save()
            messages.success(request, f'User account {"activated" if user.is_active else "deactivated"}')
            if not user.is_active:
                logout(request) if request.user.id == user_id else None
        return redirect('adminpanel:user_detail', user_id=user_id)
   
    profile = getattr(user, "profile", None)
    return render(
        request,
        "adminpanel/user_detail.html",
        {"u": user, "profile": profile},
    )




@admin_required
def products_list(request):
    from django.db.models import Count
    from users.models import Profile
    from django.contrib.auth.models import User
    from django.shortcuts import get_object_or_404
    from django.db import ProgrammingError


    user_id = request.GET.get('user_id')
    qs = Uniform.objects.all().order_by("-created_at")
   
    # Safe M2M queries - fallback if table missing
    try:
        qs = qs.annotate(assigned_count=Count('assigned_students'))
        has_m2m = True
    except ProgrammingError:
        has_m2m = False
        messages.info(request, 'Products alignment features loading... Run `python manage.py makemigrations users && migrate` for full functionality.')
   
    if user_id and has_m2m:
        try:
            user = get_object_or_404(User, id=user_id)
            profile = getattr(user, 'profile', None)
            if profile:
                qs = qs.filter(assigned_students__profile__user=user)
        except ProgrammingError:
            pass
   
    if request.method == 'POST' and has_m2m:
        action = request.POST.get('action')
        if action == 'toggle_assign':
            try:
                product_id = int(request.POST['product_id'])
                target_user_id = request.POST.get('target_user_id') or user_id
                if target_user_id:
                    target_user = User.objects.get(id=target_user_id)
                    target_profile, _ = Profile.objects.get_or_create(user=target_user)
                    product = get_object_or_404(Uniform, id=product_id)
                    if product in target_profile.assigned_products.all():
                        target_profile.assigned_products.remove(product)
                        messages.success(request, f'Removed {product.name} from {target_user.username}')
                    else:
                        target_profile.assigned_products.add(product)
                        messages.success(request, f'Added {product.name} to {target_user.username}')
                    return redirect('adminpanel:products_list', user_id=target_user_id)
            except (ProgrammingError, ValueError):
                messages.error(request, 'Assignment failed - run migrations first.')
   
    users = User.objects.filter(is_staff=False).order_by('username')
   
    context = {
        'products': qs,
        'users': users,
        'selected_user': user_id,
        'selected_user_obj': User.objects.filter(id=user_id).first() if user_id else None,
        'm2m_ready': has_m2m
    }
    return render(request, "adminpanel/products.html", context)




@admin_required
def product_detail(request, product_id: int):
    product = Uniform.objects.filter(id=product_id).first()
    if not product:
        raise Http404("Product not found")
    return render(request, "adminpanel/product_detail.html", {"p": product})




@admin_required
def orders_list(request):
    # Get all orders, ordered by most recent
    orders = Order.objects.all().order_by("-order_date")
    return render(request, "adminpanel/orders.html", {"orders": orders})




@admin_required
def order_detail(request, order_id: int):
    order = get_object_or_404(Order, id=order_id)
    return render(request, "adminpanel/order_detail.html", {"order": order})




@admin_required
def update_order_status(request, order_id: int):
    order = get_object_or_404(Order, id=order_id)
   
    if request.method == 'POST':
        old_status = order.status
       
        # Update fields
        order.customer_name = request.POST.get('customer_name', order.customer_name)
        order.email = request.POST.get('email', order.email)
        order.phone = request.POST.get('phone', order.phone)
        order.address = request.POST.get('address', order.address)
        order.total_amount = request.POST.get('total_amount', order.total_amount)
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
       
        order.save()
       
        # Send notification email
        from django.core.mail import send_mail
        subject = f'Order #{order.id} Status Update'
        message = f'Dear {order.customer_name},\n\nYour order #{order.id} status has been updated from {old_status} to {order.status.upper()}.\n\nTotal: ₱{order.total_amount}\n\nThank you!'
        send_mail(
            subject,
            message,
            'noreply@isyswear.local',
            [order.email],
            fail_silently=False,
        )
        messages.success(request, f"Order #{order.id} updated successfully. Student can now view the updated status in their account.")
        return redirect('adminpanel:order_detail', order_id=order_id)
   
    return render(request, 'adminpanel/order_update.html', {'order': order})


def admin_login_view(request):
    if request.user.is_authenticated:
        if _is_admin(request.user):
            return redirect('adminpanel:dashboard')
        messages.error(request, 'Your current account does not have administrator privileges.')
        return redirect('home')
    return redirect(f"/login/?next=/panel/")


@admin_required
def student_orders(request):
    """List non-staff users (students) who have placed orders"""
    students = User.objects.filter(
        is_staff=False,
        is_superuser=False,
        orders__isnull=False
    ).distinct().prefetch_related('orders', 'profile').order_by('-id')
    return render(request, 'adminpanel/student_orders.html', {'students': students})


@admin_required
def student_order_detail(request, user_id):
    """Detail for a student: profile + their orders"""
    user = get_object_or_404(User, id=user_id, is_staff=False)
    profile = getattr(user, 'profile', None)
    orders = user.orders.all().order_by('-order_date')
    return render(request, 'adminpanel/student_order_detail.html', {
        'student': user,
        'profile': profile,
        'orders': orders
    })


import json
from django.http import JsonResponse
from products.models import UniformSize


@admin_required
def update_size_stock(request, size_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            size = UniformSize.objects.get(id=size_id)
            size.stock = int(data['stock'])
            size.save()
            # update total stock on parent uniform
            size.uniform.stock = size.uniform.sizes.aggregate(
                total=Sum('stock'))['total'] or 0
            size.uniform.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False})




@admin_required
def product_detail(request, product_id: int):
    product = Uniform.objects.filter(id=product_id).first()
    if not product:
        raise Http404("Product not found")
   
    if request.method == 'POST':
        image_url = request.POST.get('image_url', '').strip()
        product.image_url = image_url
        product.save()
        messages.success(request, 'Image URL updated successfully.')
        return redirect('adminpanel:product_detail', product_id=product_id)


    return render(request, "adminpanel/product_detail.html", {"p": product})
