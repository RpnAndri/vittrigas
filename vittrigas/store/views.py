from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from .models import Product, Customer, Cart, CartItem
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Sum
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin

class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = get_object_or_404(Customer, user=self.request.user)
        cart, created = Cart.objects.get_or_create(customer=customer)
        context['cart'] = cart
        context['item_count'] = cart.items.aggregate(total=Sum('quantity'))['total'] or 0
        return context


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    customer = get_object_or_404(Customer, user=request.user)
    cart, created = Cart.objects.get_or_create(customer=customer)
    
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    # Get current amount of item in cart
    item_count = cart.items.aggregate(total=Sum('quantity'))['total'] or 0

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'item_count': item_count})

    # Fallback for non-AJAX requests
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def cart_detail(request):
    customer = get_object_or_404(Customer, user=request.user)
    cart, created = Cart.objects.get_or_create(customer=customer)
    return render(request, 'cart_detail.html', {'cart': cart})

@login_required
def increase_cart_item(request, item_id):
    if request.method == "POST":
        cart_item = get_object_or_404(CartItem, id=item_id, cart__customer__user=request.user)
        cart_item.quantity += 1
        cart_item.save()
        return JsonResponse({'success': True, 'quantity': cart_item.quantity})
    return JsonResponse({'success': False}, status=400)

@login_required
def decrease_cart_item(request, item_id):
    if request.method == "POST":
        cart_item = get_object_or_404(CartItem, id=item_id, cart__customer__user=request.user)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
            return JsonResponse({'success': True, 'quantity': cart_item.quantity})
        else:
            cart_item.delete()
            return JsonResponse({'success': True, 'quantity': 0})
    return JsonResponse({'success': False}, status=400)

@require_POST
@login_required
def update_cart_item_quantity(request, item_id, action):
    cart = request.user.customer.cart
    item = get_object_or_404(cart.items, id=item_id)

    if action == 'increase':
        item.quantity += 1
    elif action == 'decrease':
        item.quantity = max(1, item.quantity - 1)
    item.save()

    # Get current amout of item
    item_count = cart.items.aggregate(total=Sum('quantity'))['total'] or 0

    return JsonResponse({
        'success': True,
        'quantity': item.quantity,
        'item_count': item_count,  
    })

@login_required
def get_cart_item_count(request):
    cart = request.user.customer.cart
    item_count = cart.items.aggregate(total=Sum('quantity'))['total'] or 0
    return JsonResponse({'item_count': item_count})