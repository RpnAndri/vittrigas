from django.urls import path
from . import views
from .views import ProductListView, add_to_cart

app_name = 'store'

urlpatterns = [
    path('', views.ProductListView.as_view(), name="product"),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('checkout/', views.Checkout.as_view(), name="checkout"),
    path('paymentsuccess/', views.PaymentSuccess.as_view(), name='payment_success'),
    path('profile/<str:username>/', views.Profile.as_view(), name='profile'),
    path('cart/item/<int:item_id>/increase/', views.increase_cart_item, name='increase_cart_item'),
    path('cart/item/<int:item_id>/decrease/', views.decrease_cart_item, name='decrease_cart_item'),
    path('cart/item/<int:item_id>/remove/', views.remove_cart_item, name='remove_cart_item'),
    path('cart/item-count/', views.get_cart_item_count, name='cart_item_count'),
]