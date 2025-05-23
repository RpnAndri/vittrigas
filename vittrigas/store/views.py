from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from .models import Product, Customer, Cart, CartItem
from django.contrib.auth.decorators import login_required

# Create your views here.
class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products' 

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    customer = get_object_or_404(Customer, user=request.user)
    cart, created = Cart.objects.get_or_create(customer=customer)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def cart_detail(request):
    customer = get_object_or_404(Customer, user=request.user)
    cart, created = Cart.objects.get_or_create(customer=customer)
    return render(request, 'cart_detail.html', {'cart': cart})