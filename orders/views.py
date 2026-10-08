from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Order

@login_required
def create_order(request):
    if request.method == 'POST':
        # Create new order logic here (handled by checkout)
        messages.info(request, 'Use checkout to place orders.')
        return redirect('checkout')
    return render(request, 'pages/create_order.html')

@login_required
def list_orders(request):
    orders = request.user.orders.all()
    return render(request, 'pages/order_list.html', {'orders': orders})

@login_required
def update_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if request.method == 'POST':
        # Full order update implementation
        old_status = order.status
        
        # Update status
        new_status = request.POST.get('status')
        if new_status and new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
        
        # Update other fields if present
        order.shipping_address = request.POST.get('shipping_address', order.shipping_address)
        order.notes = request.POST.get('notes', order.notes)
        
        order.save()
        messages.success(request, f'Order #{order.id} updated: {old_status} → {order.status}')
        return redirect('orders:list_orders')  # Named URL
    return render(request, 'pages/update_order.html', {'order': order})


@login_required
def delete_order(request, order_id):
    if request.method != 'POST':
        return redirect('orders:order_history')
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order.delete()
    messages.success(request, 'Order deleted.')
    return redirect('orders:order_history')

@login_required
def order_confirmation(request):
    last_order_id = request.session.get('last_order_id')
    if last_order_id:
        order = get_object_or_404(Order, id=last_order_id, user=request.user)
    else:
        messages.warning(request, 'No recent order found.')
        order = None
    return render(request, 'pages/orderConfirmation.html', {'order': order})

@login_required
def order_details(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'pages/orderDetails.html', {'order': order})

@login_required
def order_history(request):
    orders = request.user.orders.all().order_by('-order_date')
    return render(request, 'pages/orderHistory.html', {'orders': orders})

@login_required
def order_receipt(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'pages/orderReceipt.html', {'order': order})

