from django.shortcuts import render
from store.models import Product
from django.http import HttpResponse
# Create your views here.

def store(request,category_slug=None):

    if category_slug != None:
        product = Product.objects.filter(category__slug=category_slug,is_active=True)
        count = product.count()

    else:
        product = Product.objects.filter(is_active=True)
        count = product.count()

    context = {
        'product':product,
        'product_count':count,
    }
    
    return render(request,'store/products.html',context)


def product_details(request,category_slug,product_slug):
    
    single_product = Product.objects.get(category__slug=category_slug,slug=product_slug)

    context = {
        'single_product':single_product
    }
    return render(request,'store/product_details.html',context) 