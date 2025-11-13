# store/models.py
from django.db import models
from django.contrib.auth.models import User


#  CATEGORY MODEL (Add this at the top)
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


#  PRODUCT MODEL
class Product(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )  # ✅ Connect each product to a category
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


#  ORDER MODEL
class Order(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='orders'
    )
    name = models.CharField(max_length=255)
    email = models.EmailField()
    address = models.TextField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} by {self.name}"

#  ORDER ITEM MODEL
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def get_total(self):
        return self.quantity * self.price

#  ORDER REVIEW

class Review(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=5)  # ⭐ 1–5 scale
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s review for {self.product.name}"


    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
