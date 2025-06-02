from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()

class Product(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=99, default="")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    rating = models.PositiveIntegerField(default=0)
    quantity = models.PositiveIntegerField(default=0)
    img = models.ImageField(upload_to='products/', default='products/tree.png')

    def __str__(self):
        return self.name

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.user.username

class Cart(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.customer.user.username

class CartItem(models.Model):
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return str(self.cart.customer.user.username) + "-" + str(self.product.name)