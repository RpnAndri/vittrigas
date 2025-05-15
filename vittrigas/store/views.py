from django.shortcuts import render
from django.views.generic import ListView
from . import models

# Create your views here.
class Product(ListView):
    model = models.Product
    template_name = 'product_list.html'
    context_object_name = 'products' 