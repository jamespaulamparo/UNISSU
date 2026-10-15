from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from products.models import Uniform
from orders.models import Order, OrderItem
from users.models import Profile

def cart_view(request):
    raw = request.session.get('cart', {})
    items = []
    total = 0
    for pk_str, data in raw.items():
        try:
            pk = int(pk_str)
            uniform = get_object_or_404(Uniform, id=pk)
        except ValueError:
            continue
        if isinstance(data, dict):
            qty = data.get('quantity', 1)
            size = data.get('size', uniform.get_size_display())
        else:
            qty = data
            size = uniform.get_size_display()
        item_total = uniform.price * qty
        items.append({
            'uniform': uniform,
            'quantity': qty,
            'selected_size': size,
            'total_price': item_total,
        })
        total += item_total
    return render(request, 'pages/cart.html', {'cart_items': items, 'cart_total': total})

def checkout(request):
    if not request.user.is_authenticated:
        messages.info(request, "Please log in with your student account or register to complete your order reservation.")
        return redirect('/login/?next=/cart/checkout/')

    raw = request.session.get('cart', {})
    items = []
    total = 0
    for pk_str, data in raw.items():
        try:
            pk = int(pk_str)
            uniform = get_object_or_404(Uniform, id=pk)
        except (ValueError, Http404):
            continue
        if isinstance(data, dict):
            qty = data.get('quantity', 1)
            size = data.get('size', uniform.get_size_display())
        else:
            qty = data
            size = uniform.get_size_display()
        item_total = uniform.price * qty
        items.append({
            'uniform': uniform,
            'quantity': qty,
            'selected_size': size,
            'total_price': item_total,
        })
        total += item_total

    profile = getattr(request.user, 'profile', None)

    if request.method == 'POST':
        # ── "Delete" single item button ───────────────────────────
        if 'delete_item' in request.POST:
            item_id = request.POST.get('item_id')
            cart = request.session.get('cart', {})
            cart.pop(str(item_id), None)
            request.session['cart'] = cart
            messages.info(request, "Item removed from your cart.")
            return redirect('checkout')

        # Payment options extraction
        payment_method = request.POST.get('payment_method', 'cash')
        if payment_method not in ['cash', 'online']:
            payment_method = 'cash'

        payment_reference = request.POST.get('payment_reference', '').strip()
        payment_receipt = request.FILES.get('payment_receipt')
        contact_phone = request.POST.get('phone', '').strip() or (profile.phone_number if profile else '')

        # Online payment requires proof
        if payment_method == 'online':
            if not payment_reference:
                messages.error(request, "Please enter your payment reference / transaction number.")
                return render(request, 'pages/checkout.html', {'cart_items': items, 'cart_total': total, 'profile': profile})
            if not payment_receipt:
                messages.error(request, "Please upload a screenshot or image of your payment receipt.")
                return render(request, 'pages/checkout.html', {'cart_items': items, 'cart_total': total, 'profile': profile})

        customer_name = profile.full_name if (profile and profile.full_name) else (request.user.get_full_name() or request.user.username)
        student_id_val = profile.student_id if profile else ''
        course_year_val = profile.course_year if profile else ''

        # ── "Order All Items" button ──────────────────────────────
        if 'place_order_all' in request.POST:
            if not items:
                messages.error(request, "Your cart is currently empty.")
                return redirect('cart')

            order = Order.objects.create(
                user=request.user,
                customer_name=customer_name,
                email=request.user.email,
                phone=contact_phone,
                student_id=student_id_val,
                course_year=course_year_val,
                pickup_location='DMMMSU NLUC CIS Faculty Office',
                address='Counter Pickup',
                payment_method=payment_method,
                payment_reference=payment_reference,
                payment_receipt=payment_receipt,
                total_amount=total,
                status='pending',
            )
            for item in items:
                OrderItem.objects.create(
                    order=order,
                    product_id=item['uniform'].id,
                    product_name=item['uniform'].name,
                    size=item['selected_size'],
                    quantity=item['quantity'],
                    price=item['uniform'].price,
                )
            # Clear entire cart
            request.session['cart'] = {}
            request.session['last_order_id'] = order.id
            messages.success(request, f"Order placed successfully! Order Claim Code: {order.claim_code}")
            return redirect('orders:order_confirmation')

        # ── "Order" single item button ────────────────────────────
        elif 'place_order_single' in request.POST:
            item_id = request.POST.get('item_id')
            single_item = next(
                (i for i in items if str(i['uniform'].id) == str(item_id)), None
            )
            if single_item:
                order = Order.objects.create(
                    user=request.user,
                    customer_name=customer_name,
                    email=request.user.email,
                    phone=contact_phone,
                    student_id=student_id_val,
                    course_year=course_year_val,
                    pickup_location='DMMMSU NLUC CIS Faculty Office',
                    address='Counter Pickup',
                    payment_method=payment_method,
                    payment_reference=payment_reference,
                    payment_receipt=payment_receipt,
                    total_amount=single_item['total_price'],
                    status='pending',
                )
                OrderItem.objects.create(
                    order=order,
                    product_id=single_item['uniform'].id,
                    product_name=single_item['uniform'].name,
                    size=single_item['selected_size'],
                    quantity=single_item['quantity'],
                    price=single_item['uniform'].price,
                )
                # Remove only that item from cart
                cart = request.session.get('cart', {})
                cart.pop(str(item_id), None)
                request.session['cart'] = cart
                request.session['last_order_id'] = order.id
                messages.success(request, f"Order placed successfully! Order Claim Code: {order.claim_code}")
                return redirect('orders:order_confirmation')

    return render(request, 'pages/checkout.html', {
        'cart_items': items,
        'cart_total': total,
        'profile': profile
    })

def add_to_cart(request, pk):
    if request.method != 'POST':
        return redirect('uniform_detail', pk=pk)
    
    uniform = get_object_or_404(Uniform, id=pk)
    
    try:
        qty = int(request.POST.get('quantity', 1))
        if qty < 1:
            qty = 1
    except ValueError:
        qty = 1
    
    size = request.POST.get('size', uniform.get_size_display())
    
    cart = request.session.get('cart', {})
    pk_str = str(pk)
    if pk_str in cart and isinstance(cart[pk_str], dict):
        cart[pk_str]['quantity'] += qty
    else:
        cart[pk_str] = {'quantity': qty, 'size': size}
    request.session['cart'] = cart
    msgs = request.session.get('cart_messages', [])
    msgs.append('Added item to cart.')
    request.session['cart_messages'] = msgs
    return redirect('cart')

def remove_from_cart(request, pk):
    if request.method != 'POST':
        return redirect('cart')
    
    cart = request.session.get('cart', {})
    pk_str = str(pk)
    if pk_str in cart:
        del cart[pk_str]
        request.session['cart'] = cart
        msgs = request.session.get('cart_messages', [])
        msgs.append('Item removed from cart.')
        request.session['cart_messages'] = msgs
    
    return redirect('cart')
