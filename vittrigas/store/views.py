from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, TemplateView, FormView
from django.views.generic.edit import FormMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import PaymentForm, ProfileForm
from .models import Product, Customer, Cart, CartItem

User = get_user_model()
from django.http import JsonResponse, HttpResponseBadRequest
from django.db.models import Sum
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string

from .models import Product, Customer, Cart, CartItem


class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(name__icontains=query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
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
        cart_html = render_to_string('partials/cart_dropdown.html', {'cart': cart}, request=request)
        return JsonResponse({'item_count': item_count, 'cart_html': cart_html})

    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def get_cart_dropdown(request):
    customer = get_object_or_404(Customer, user=request.user)
    cart, _ = Cart.objects.get_or_create(customer=customer)
    cart_html = render_to_string('partials/cart_dropdown.html', {'cart': cart}, request=request)
    return JsonResponse({'cart_html': cart_html})

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

@require_POST
@login_required
def remove_cart_item(request, item_id):
    cart = request.user.customer.cart
    cart_item = get_object_or_404(CartItem, id=item_id, cart__customer__user=request.user)
    cart_item.delete()

    item_count = cart.items.aggregate(total=Sum('quantity'))['total'] or 0

    return JsonResponse({
        'success': True,
        'quantity': 0,
        'item_count': item_count,
    })

@login_required
def get_cart_item_count(request):
    cart = request.user.customer.cart
    item_count = cart.items.aggregate(total=Sum('quantity'))['total'] or 0
    return JsonResponse({'item_count': item_count})

class Checkout(LoginRequiredMixin, FormMixin, DetailView):
    model = Cart
    template_name = 'checkout.html'
    context_object_name = 'cart'
    form_class = PaymentForm

    def get_object(self):
        return self.request.user.customer.cart

    def get_success_url(self):
        return reverse_lazy('store:payment_success') 

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        
        if form.is_valid():
            # Handle mock or real payment here
            # These are all strings
            card_number = form.cleaned_data['card_number']
            card_holder = form.cleaned_data['card_holder']
            expiry = form.cleaned_data['expiry']
            cvc = form.cleaned_data['cvc']

            # Delete the contents of the cart indicating that you bought it
            CartItem.objects.filter(cart=self.object).delete()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()

        address = get_object_or_404(Customer, user=self.request.user).address
        if address == '':
            context['address_error'] = True

        return context

class PaymentSuccess(LoginRequiredMixin, TemplateView):
    template_name = 'payment_success.html'

class Profile(FormMixin, DetailView):
    template_name = 'accounts/profile.html'
    form_class = ProfileForm
    model = User
    context_object_name = 'profile'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_success_url(self):
        return reverse('store:profile', kwargs={'username': self.get_object().username})
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        profile_user = self.get_object()
        customer = Customer.objects.get(user=profile_user)
        kwargs['instance'] = profile_user
        kwargs['customer'] = customer
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.user != self.object:
            return self.handle_no_permission()

        form = self.get_form()
        if form.is_valid():
            form.save(self.object, self.object.customer)

            if form.cleaned_data.get('password'):
                update_session_auth_hash(request, self.object)
                
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user == self.get_object():
            context['form'] = self.get_form()
        return context
