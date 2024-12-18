from django.shortcuts import render
from store.models import *

def index(request):
    product = Product.objects.all()

    context = {
        'product':product,
    }
    
    return render(request,'index.html',context)