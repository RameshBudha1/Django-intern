from django.contrib import admin
from . models import Products,Category

# Register your models here.

class ProductsAdmin(admin.ModelAdmin):
    list_display = ('product_name','product_price','created_at',)
    list_filter = ('category','created_at',)

admin.site.register(Products,ProductsAdmin)
admin.site.register(Category)
