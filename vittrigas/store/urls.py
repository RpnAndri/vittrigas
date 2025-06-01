from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.ProductListView.as_view(), name="product"),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/item/<int:item_id>/increase/', views.increase_cart_item, name='increase_cart_item'),
    path('cart/item/<int:item_id>/decrease/', views.decrease_cart_item, name='decrease_cart_item'),
    path('cart/update/<int:item_id>/<str:action>/', views.update_cart_item_quantity, name='update_cart_item'),
    path('cart/item-count/', views.get_cart_item_count, name='cart_item_count'),
]