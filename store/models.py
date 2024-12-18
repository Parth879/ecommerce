from django.db import models

# Create your models here.

class Product(models.Model):
    product_name = models.CharField(max_length=100)
    product_discription = models.CharField(max_length=255)
    product_price = models.IntegerField()
    product_image = models.ImageField(upload_to='product_image/')
    product_stock = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product_name