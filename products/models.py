from django.db import models
from django.utils.text import slugify
from base.models import Basemodel

class Category(Basemodel):
    categroy_name=models.CharField(max_length=100)
    slug=models.SlugField(unique=True, null=True, blank=True)
    category_image=models.ImageField(upload_to="categories")
    
    def save(self , *args , **kwargs):
        self.slug = slugify(self.categroy_name)
        super(Category ,self).save(*args , **kwargs)
        
    def __str__(self) -> str:
        return self.categroy_name
    
class ColorVariant(Basemodel):
    color_name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.color_name

class SizeVariant(Basemodel):
    size_name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)
    
    def __str__(self) -> str:
        return self.size_name

   
class Product(Basemodel):
    product_name=models.CharField(max_length=100)
    slug=models.SlugField(unique=True, null=True, blank=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name="products")
    price=models.IntegerField()
    product_description=models.TextField()
    color_variant = models.ManyToManyField(ColorVariant , blank=True)
    size_variant = models.ManyToManyField(SizeVariant , blank=True)
    def save(self , *args , **kwargs):
        self.slug = slugify(self.product_name)
        super(Product ,self).save(*args , **kwargs)
    def __str__(self) -> str:
        return self.product_name
    
class ProductImage(Basemodel):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name="product_images")
    product_image=models.ImageField(upload_to="product")
    
    
