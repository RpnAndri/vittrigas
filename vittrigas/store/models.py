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