from django.shortcuts import render
from store.models import Product
# Create your views here.

def store(request,category_slug=None):

    if category_slug != None:
        product = Product.objects.filter(category__slug=category_slug,is_active=True)
    else:
        product = Product.objects.filter(is_active=True)
    
    return render(request,'store/products.html',{'product':product})