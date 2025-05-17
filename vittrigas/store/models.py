from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()

class Product(models.Model):
    name = models.CharField(max_length=20)
    price = models.PositiveIntegerField(default=0)
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
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_total_price(self):
        return self.product.price * self.quantity