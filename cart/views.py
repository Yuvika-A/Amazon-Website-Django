from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product, Order, OrderItem
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# -----------------------------
# Helper functions
# -----------------------------
def _get_cart(request):
    """Retrieve the shopping cart from session"""
    return request.session.get('cart', {})

def _save_cart(request, cart):
    """Save the cart back into session"""
    request.session['cart'] = cart
    request.session.modified = True


# -----------------------------
# Cart Operations
# -----------------------------
def add_to_cart(request, product_id):
    """Add a product to cart (or increase if exists)"""
    cart = _get_cart(request)
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    _save_cart(request, cart)
    return redirect('home')


def increase_quantity(request, product_id):
    """Increase quantity of a product in the cart"""
    cart = _get_cart(request)
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    _save_cart(request, cart)
    return redirect('view_cart')


def decrease_quantity(request, product_id):
    """Decrease quantity of a product (remove if 0)"""
    cart = _get_cart(request)
    qty = cart.get(str(product_id), 0)
    if qty > 1:
        cart[str(product_id)] = qty - 1
    else:
        cart.pop(str(product_id), None)
    _save_cart(request, cart)
    return redirect('view_cart')


def remove_item(request, product_id):
    """Remove a product entirely from the cart"""
    cart = _get_cart(request)
    cart.pop(str(product_id), None)
    _save_cart(request, cart)
    return redirect('view_cart')


def clear_cart(request):
    """Clear the entire shopping cart"""
    request.session['cart'] = {}
    request.session.modified = True
    return redirect('view_cart')


# -----------------------------
# Cart Page
# -----------------------------
def view_cart(request):
    """Display cart items and total"""
    cart = _get_cart(request)
    products = []
    total = 0

    for pid, qty in cart.items():
        product = get_object_or_404(Product, pk=int(pid))
        product.quantity = qty
        product.total_price = product.price * qty
        products.append(product)
        total += product.total_price

    return render(request, 'cart/cart.html', {
        'products': products,
        'total': total
    })


# -----------------------------
# Checkout Page
# -----------------------------
@login_required
def checkout(request):
    """Display checkout page and handle order confirmation"""
    cart = request.session.get('cart', {})
    products = []
    total = 0

    for pid, qty in cart.items():
        product = get_object_or_404(Product, pk=int(pid))
        product.quantity = qty
        product.total_price = product.price * qty
        products.append(product)
        total += product.total_price

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')

        if not name or not email or not address:
            messages.error(request, "Please fill in all fields.")
        else:
            # Create order for logged-in user
            order = Order.objects.create(
                user=request.user if request.user.is_authenticated else None,
                name=name,
                email=email,
                address=address,
                total=total
            )

            # Create individual order items
            for p in products:
                OrderItem.objects.create(
                    order=order,
                    product=p,
                    quantity=p.quantity,
                    price=p.price
                )

            # Clear cart after placing order
            request.session['cart'] = {}
            request.session.modified = True

            messages.success(request, "Order placed successfully!")
            return render(request, 'cart/order_success.html', {'order': order})

    return render(request, 'cart/checkout.html', {
        'products': products,
        'total': total
    })


# -----------------------------
# 🧾 Order History Page
# -----------------------------
@login_required
def order_history(request):
    """Display all past orders for the logged-in user"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'cart/order_history.html', {'orders': orders})
