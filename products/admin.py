from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Category)

class ProductImageAdmin(admin.StackedInline):
    model =ProductImage

class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name' , 'price' ]
    inlines = [ProductImageAdmin]


admin.site.register(Product ,ProductAdmin)

admin.site.register(ProductImage)
