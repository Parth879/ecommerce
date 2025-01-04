from django.shortcuts import render, redirect
from store.models import Product
from django.http import HttpResponse
from carts.models import *
# Create your views here.

def _cart_id(request):
    cart = request.session.session_key
    if cart is None:
        cart = request.session.create()
    return cart


def add_cart(request,product_id):
    product = Product.objects.get(id=product_id)

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))

    try:
        cart_products = CartItem.objects.get(product=product,cart=cart)
        cart_products.quantity += 1
        cart_products.save()
    except:
        cart_products = CartItem.objects.create(
            product = product,
            cart = cart,
            quantity = 1
        )

    return redirect('cart')

def cart(request):
    total = 0

    cart_items = CartItem.objects.filter(cart__cart_id=_cart_id(request))
    
    # total += (cart_items.product.product_price * cart_items.quantity)
    
    context = {
        'cart_items' : cart_items,
        'total':total
    }

    return render(request,'store/cart.html',context)