from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Sum
from django.views.decorators.http import require_POST

from .models import Product, Customer, Cart, CartItem


class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = get_object_or_404(Customer, user=self.request.user)
        cart, _ = Cart.objects.get_or_create(customer=customer)
        context['cart'] = cart
        context['item_count'] = cart.items.aggregate(total=Sum('quantity'))['total'] or 0
        return context


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    customer = get_object_or_404(Customer, user=request.user)
    cart, _ = Cart.objects.get_or_create(customer=customer)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    item_count = cart.items.aggregate(total=Sum('quantity'))['total'] or 0

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'item_count': item_count})

    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def cart_detail(request):
    customer = get_object_or_404(Customer, user=request.user)
    cart, _ = Cart.objects.get_or_create(customer=customer)
    return render(request, 'cart_detail.html', {'cart': cart})


@require_POST
@login_required
def increase_cart_item(request, item_id):
    cart = request.user.customer.cart
    cart_item = get_object_or_404(CartItem, id=item_id, cart__customer__user=request.user)
    cart_item.quantity += 1
    cart_item.save()
    item_count = cart.items.aggregate(total=Sum('quantity'))['total'] or 0
    return JsonResponse({
        'success': True,
        'quantity': cart_item.quantity,
        'item_count': item_count,
    })


@require_POST
@login_required
def decrease_cart_item(request, item_id):
    cart = request.user.customer.cart
    cart_item = get_object_or_404(CartItem, id=item_id, cart__customer__user=request.user)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
        quantity = cart_item.quantity
    else:
        cart_item.delete()
        quantity = 0

    item_count = cart.items.aggregate(total=Sum('quantity'))['total'] or 0

    return JsonResponse({
        'success': True,
        'quantity': quantity,
        'item_count': item_count,
    })


@login_required
def get_cart_item_count(request):
    cart = request.user.customer.cart
    item_count = cart.items.aggregate(total=Sum('quantity'))['total'] or 0
    return JsonResponse({'item_count': item_count})