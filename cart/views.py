from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from products.models import Uniform
from orders.models import Order, OrderItem  # ← this line must be correct

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

@login_required
def checkout(request):
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

    if request.method == 'POST':
        # ── "Order All Items" button ──────────────────────────────
        if 'place_order_all' in request.POST:
            order = Order.objects.create(
                user=request.user,
                customer_name=request.user.get_full_name() or request.user.username,
                email=request.user.email,
                address='CIS Faculty Pickup',
                phone='',
                total_amount=total,
                status='pending',
            )
            for item in items:
                OrderItem.objects.create(
                    order=order,
                    product_id=item['uniform'].id,
                    product_name=item['uniform'].name,
                    quantity=item['quantity'],
                    price=item['uniform'].price,
                )
            # Clear entire cart
            request.session['cart'] = {}
            request.session['last_order_id'] = order.id
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
                    customer_name=request.user.get_full_name() or request.user.username,
                    email=request.user.email,
                    address='CIS Faculty Pickup',
                    phone='',
                    total_amount=single_item['total_price'],
                    status='pending',
                )
                OrderItem.objects.create(
                    order=order,
                    product_id=single_item['uniform'].id,
                    product_name=single_item['uniform'].name,
                    quantity=single_item['quantity'],
                    price=single_item['uniform'].price,
                )
                # Remove only that item from cart
                cart = request.session.get('cart', {})
                cart.pop(str(item_id), None)
                request.session['cart'] = cart
                request.session['last_order_id'] = order.id
            return redirect('orders:order_confirmation')

        # ── "Delete" single item button ───────────────────────────
        elif 'delete_item' in request.POST:
            item_id = request.POST.get('item_id')
            cart = request.session.get('cart', {})
            cart.pop(str(item_id), None)
            request.session['cart'] = cart
            return redirect('checkout')

    return render(request, 'pages/checkout.html', {'cart_items': items, 'cart_total': total})

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
