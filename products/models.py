from django.db import models
from django.utils.text import slugify
from base.models import Basemodel

CATEGORY_TYPE_CHOICES = (
    ('MEN', 'Men'),
    ('WOMEN', 'Women'),
)

class Category(Basemodel):
    categroy_name=models.CharField(max_length=100)
    slug=models.SlugField(unique=True, null=True, blank=True)
    category_type=models.CharField(max_length=10, choices=CATEGORY_TYPE_CHOICES, default='MEN')
    
    def save(self, *args, **kwargs):
        base_slug = slugify(self.categroy_name)
        slug = base_slug
        n = 1
        while Category.objects.filter(slug=slug).exclude(pk=self.pk).exists():
            slug = f"{base_slug}-{n}"
            n += 1
        self.slug = slug
        super(Category, self).save(*args, **kwargs)
        
    def __str__(self) -> str:
        return f"{self.categroy_name} ({self.get_category_type_display()})"
    
class ColorVariant(Basemodel):
    color_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self) -> str:
        return self.color_name

class SizeVariant(Basemodel):
    size_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    def __str__(self) -> str:
        return self.size_name

   
class Product(Basemodel):
    product_name=models.CharField(max_length=100)
    slug=models.SlugField(unique=True, null=True, blank=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name="products")
    price=models.DecimalField(max_digits=10, decimal_places=2)
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
    
    
