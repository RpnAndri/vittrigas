from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.Product.as_view(), name="product"),
]