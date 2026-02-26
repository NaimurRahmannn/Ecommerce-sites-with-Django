from django.urls import path
from products.views import (
    get_product,
    add_to_cart,
    cart,
    remove_from_cart,
    update_cart,
    buy_now,
    checkout,
)

urlpatterns = [
    path('cart/', cart, name="cart"),
    path('cart/update/', update_cart, name="update_cart"),
    path('checkout/', checkout, name="checkout"),
    path('buy-now/<slug>/', buy_now, name="buy_now"),
    path('add-to-cart/<slug>/', add_to_cart, name="add_to_cart"),
    path('remove-from-cart/<slug>/', remove_from_cart, name="remove_from_cart"),
    path('<slug>/', get_product, name="get_product"),
]
