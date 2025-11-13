from django.urls import path
from . import views

urlpatterns = [
    path('cart', views.view_cart, name='view_cart'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('increase/<int:product_id>/', views.increase_quantity, name='increase_quantity'),
    path('decrease/<int:product_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('remove/<int:product_id>/', views.remove_item, name='remove_item'),
    path('clear/', views.clear_cart, name='clear_cart'),
    path('checkout/', views.checkout, name='checkout'),  
    path('orders/', views.order_history, name='order_history'),
]
