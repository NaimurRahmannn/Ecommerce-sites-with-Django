from django.db import models

from base.models import Basemodel

class Category(Basemodel):
    categroy_name=models.CharField(max_length=100)
    category_image=models.ImageField(upload_to="categories")
    
class Product(Basemodel):
    product_name=models.CharField(max_length=100)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name="products")
    price=models.IntegerField()
    product_description=models.TextField()
    
class ProductImage(Basemodel):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name="product_images")
    product_image=models.ImageField(upload_to="product")
    
    
