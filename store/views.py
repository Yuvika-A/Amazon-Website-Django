# store/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Category, Review


# --------------------------------------------
# 🏠 HOME PAGE (Search + Category Filter)
# --------------------------------------------
def home(request):
    query = request.GET.get('q', '')
    selected_category = request.GET.get('category', '')

    # Start with all products
    products = Product.objects.all()

    # 🔍 Filter by search query (name or description)
    if query:
        products = products.filter(name__icontains=query) | products.filter(description__icontains=query)

    # 🏷️ Filter by category
    if selected_category:
        products = products.filter(category_id=selected_category)

    # 📦 Get all categories for dropdown
    categories = Category.objects.all()

    # 🛒 Cart info
    cart = request.session.get('cart', {})
    cart_count = sum(cart.values())

    context = {
        'products': products,
        'query': query,
        'categories': categories,
        'selected_category': int(selected_category) if selected_category else '',
        'cart_count': cart_count,
    }

    return render(request, 'store/home.html', context)


# --------------------------------------------
# 🧾 PRODUCT DETAIL PAGE (with reviews)
# --------------------------------------------
def product_detail(request, product_id):
    """Display a single product with its reviews"""
    product = get_object_or_404(Product, id=product_id)
    reviews = product.reviews.all().order_by('-created_at')

    # ⭐ Calculate average rating
    avg_rating = 0
    avg_rating = (
        sum(r.rating for r in reviews) / len(reviews)
        if reviews else 0
    )
    # 🟢 Fetch related products (same category)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]

    context = {
        'product': product,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'related_products': related_products,

    }
    return render(request, 'store/product_detail.html', context)


# --------------------------------------------
# ✍️ ADD REVIEW PAGE (for logged-in users)
# --------------------------------------------
@login_required
def add_review(request, product_id):
    """Allow logged-in users to submit a product review"""
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        rating = int(request.POST.get('rating', 5))
        comment = request.POST.get('comment', '')

        # Prevent duplicate reviews by same user
        existing_review = Review.objects.filter(user=request.user, product=product)
        if existing_review.exists():
            messages.error(request, "You have already reviewed this product.")
        else:
            Review.objects.create(
                product=product,
                user=request.user,
                rating=rating,
                comment=comment
            )
            messages.success(request, "✅ Your review has been submitted successfully!")

        return redirect('product_detail', product_id=product.id)

    return render(request, 'store/add_review.html', {'product': product})


# --------------------------------------------
# 🧾 OPTIONAL: DISPLAY ALL REVIEWS BY USER
# --------------------------------------------
@login_required
def my_reviews(request):
    """Display all reviews written by the logged-in user"""
    reviews = Review.objects.filter(user=request.user).select_related('product').order_by('-created_at')
    return render(request, 'store/my_reviews.html', {'reviews': reviews})
