from django.urls import path
from carts.views import *

urlpatterns = [
    path('',cart,name='cart'),
    path('add_cart/<product_id>/',add_cart,name='add_cart'),
]