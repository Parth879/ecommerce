from django.shortcuts import get_object_or_404, render, redirect
from store.models import Product, Variation
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

    product_variation = []
    if request.method == 'POST':
        for item in request.POST:      
            key = item
            value = request.POST[key]
            
            try:
                variation = Variation.objects.get(product=product,variation_category__iexact=key,variation_value__iexact=value)
                product_variation.append(variation)
            except:
                pass

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))

    is_product_var_exi = CartItem.objects.filter(product=product,cart=cart)
    
    if is_product_var_exi:
        cart_items = CartItem.objects.filter(product=product,cart=cart)
        exi_var_list = []
        id= []
        
        for item in cart_items:
            existing_variations = item.variations.all()
            exi_var_list.append(list(existing_variations))
            id.append(item.id)
            
        if product_variation in exi_var_list:
            index = exi_var_list.index(product_variation)
            item_id = id[index]
            item = CartItem.objects.get(product=product,id=item_id)
            item.quantity += 1 
            item.save()
        else:
            cart_products = CartItem.objects.create(product = product,cart = cart,quantity = 1)
            if len(product_variation) > 0:
                cart_products.variations.clear()
                cart_products.variations.add(*product_variation)
    else:
        cart_products = CartItem.objects.create(
            product = product,
            cart = cart,
            quantity = 1
        )
        if len(product_variation) > 0:
            cart_products.variations.clear()
            cart_products.variations.add(*product_variation)

    return redirect('cart')

def remove_cart(request,product_id,cart_item_id):
    products = get_object_or_404(Product,id=product_id)
    
    carts = Cart.objects.get(cart_id=_cart_id(request))
    cart_item = CartItem.objects.get(product=products,cart=carts,id=cart_item_id)
    if cart_item.quantity > 1:
        cart_item.quantity -=1
        cart_item.save()
        return redirect('cart')
    else:
        cart_item.delete()
        return redirect('cart')

def remove_cart_item(request,product_id,cart_item_id):
    products = get_object_or_404(Product,id=product_id)
    carts = Cart.objects.get(cart_id=_cart_id(request))
    cart_item = CartItem.objects.get(product=products, cart=carts, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')

def cart(request):
    total = 0

    cart_items = CartItem.objects.filter(cart__cart_id=_cart_id(request))
    for i in cart_items:
        total += (i.product.product_price * i.quantity)
    
    tax = (2 * total)/100
    grand_total = total + tax
   
    context = {
        'cart_items' : cart_items,
        'total':total,
        'tax': tax,
        'grand_total': grand_total,
    }

    return render(request,'store/cart.html',context)