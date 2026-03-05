from django.contrib import admin

# Register your models here.
from .models import *

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['categroy_name', 'category_type', 'slug']
    list_filter = ['category_type']
    prepopulated_fields = {'slug': ('categroy_name',)}

class ProductImageAdmin(admin.StackedInline):
    model =ProductImage

class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'price']
    inlines = [ProductImageAdmin]
    filter_horizontal = ['size_variant', 'color_variant']

@admin.register(ColorVariant)
class ColorVariantAdmin(admin.ModelAdmin):
    list_display = ['color_name' , 'price']
    model = ColorVariant

@admin.register(SizeVariant)
class SizeVariantAdmin(admin.ModelAdmin):
    list_display = ['size_name' , 'price']

    model = SizeVariant


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ['product', 'product_name', 'size', 'quantity', 'price', 'line_total']
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'first_name', 'last_name', 'email', 'payment_method', 'total', 'created_at']
    list_filter = ['payment_method', 'created_at']
    search_fields = ['order_number', 'email', 'first_name', 'last_name', 'transaction_id']
    readonly_fields = ['order_number']
    inlines = [OrderItemInline]

admin.site.register(Product ,ProductAdmin)

admin.site.register(ProductImage)
