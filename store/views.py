from django.shortcuts import render
from carts.views import _cart_id
from store.models import Product
from carts.models import CartItem
from django.db.models import Q
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

    in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request),product=single_product).exists()
    
    context = {
        'single_product':single_product,
        'in_cart':in_cart,
    }
    return render(request,'store/product_details.html',context) 


def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        
        if keyword:
            product = Product.objects.filter(Q(product_name__icontains=keyword) | Q(product_discription__icontains=keyword))
            count = product.count()

        context = {
            'product' : product,
            'product_count':count
        }
        return render(request,'store/products.html',context)