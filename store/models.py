from django.db import models
from category.models import Category
from django.urls import reverse
# Create your models here.

class Product(models.Model):
    product_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200,unique=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    product_image = models.ImageField(upload_to='product_image/')
    product_price = models.IntegerField()
    product_stock = models.IntegerField()
    product_discription = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.product_name
    
    def get_url(self):
        return reverse('product_details',args=[self.category.slug,self.slug])