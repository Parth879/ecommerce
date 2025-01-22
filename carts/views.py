from django.shortcuts import get_object_or_404, render, redirect
from store.models import Product, Variation
from django.http import HttpResponse
from carts.models import *
from django.contrib.auth.decorators import login_required
# Create your views here.

def _cart_id(request):
    cart = request.session.session_key
    if cart is None:
        cart = request.session.create()
    return cart


def add_cart(request,product_id):

    product = Product.objects.get(id=product_id)

    product_variations = []
    if request.method == 'POST':
        for item in request.POST:      
            key = item
            value = request.POST[key]
            
            try:
                variation = Variation.objects.get(product=product,variation_category__iexact=key,variation_value__iexact=value)
                product_variations.append(variation)
            except:
                pass
        
    if request.user.is_authenticated:

        # Check if the product with the same variations exists in the cart
        cart_items = CartItem.objects.filter(product=product, user=request.user)
        
        for cart_item in cart_items:
            existing_variations = list(cart_item.variations.all())
            if product_variations == existing_variations:
                cart_item.quantity += 1
                cart_item.save()
                break
        else:
            # Create a new cart item if no matching variations exist
            cart_item = CartItem.objects.create(
                product=product,
                user=request.user,
                quantity=1,
                cart=None
            )
            if product_variations:
                cart_item.variations.add(*product_variations)
    else:   
        cart, created = Cart.objects.get_or_create(cart_id=_cart_id(request))

        # Check if the product with the same variations exists in the cart
        cart_items = CartItem.objects.filter(product=product, cart=cart)
        
        for cart_item in cart_items:
            existing_variations = list(cart_item.variations.all())
            if product_variations == existing_variations:
                cart_item.quantity += 1
                cart_item.save()
                break
        else:
            # Create a new cart item if no matching variations exist
            cart_item = CartItem.objects.create(
                product=product,
                cart=cart,
                user=None,
                quantity=1
            )
            if product_variations:
                cart_item.variations.add(*product_variations)

    return redirect('cart')

def pluse_cart(request,product_id,cart_item_id):
    products = get_object_or_404(Product,id=product_id)

    try :
        cart_item = CartItem.objects.get(user=request.user,product=products,id=cart_item_id)
    except:
        carts = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=products,cart=carts,id=cart_item_id)
    
    cart_item.quantity +=1
    cart_item.save()
    return redirect('cart')

def remove_cart(request,product_id,cart_item_id):
    products = get_object_or_404(Product,id=product_id)
    

    try :
        cart_item = CartItem.objects.get(user=request.user,product=products,id=cart_item_id)
    except:
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

    try :
        cart_item = CartItem.objects.get(user=request.user,product=products,id=cart_item_id)
    except:
        carts = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=products,cart=carts,id=cart_item_id)

    cart_item.delete()
    return redirect('cart')

def cart(request):
    total = 0

    try:
        cart_items = CartItem.objects.filter(user=request.user)
    except:
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

@login_required(login_url='login')
def checkout(request):
    total = 0
    cart_items = CartItem.objects.filter(user=request.user)

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

    return render(request,'store/checkout.html',context)