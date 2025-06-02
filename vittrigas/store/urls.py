from django.urls import path
from . import views
from .views import ProductListView, add_to_cart

app_name = 'store'

urlpatterns = [
    path('', views.ProductListView.as_view(), name="product"),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('checkout/', views.Checkout.as_view(), name="checkout"),
    path('paymentsuccess/', views.PaymentSuccess.as_view(), name='payment_success'),
    path('profile/<str:username>/', views.Profile.as_view(), name='profile'),
    path('products/', ProductListView.as_view(), name='product_list'),
]