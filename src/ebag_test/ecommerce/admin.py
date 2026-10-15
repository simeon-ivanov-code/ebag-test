from django.contrib import admin

from .models import *

class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = ['id', 'name']
    search_fields = ['name']

class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ['id', 'sku', 'title', 'category', 'description', 'price', 'image']
    search_fields = ['sku', 'title', 'description']
    list_filter = ['category']

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
