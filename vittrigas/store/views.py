from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from .models import Product, Customer, Cart, CartItem
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Sum

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
    
    # Gesamtanzahl aller Items im Warenkorb (Summe quantity)
    from django.db.models import Sum
    item_count = cart.items.aggregate(total=Sum('quantity'))['total'] or 0

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'item_count': item_count})

    # Fallback: bei normalem Request weiterleiten
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
            # Optional: Item löschen, wenn Menge 0 erreichen soll
            cart_item.delete()
            return JsonResponse({'success': True, 'quantity': 0})
    return JsonResponse({'success': False}, status=400)