from django.contrib import admin
from store.models import Product

# Register your models here.

class AdminProduct(admin.ModelAdmin):
    list_display = ['product_name']
    prepopulated_fields = {'slug':('product_name',)}

admin.site.register(Product,AdminProduct)