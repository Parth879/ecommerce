from django.db import models

# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=200,unique=True)
    slug = models.SlugField(max_length=200,unique=True)
    image = models.ImageField(upload_to='category_image')
    
    def __str__(self):
        return self.category_name

