from django.contrib import admin
from .models import Brand, Product
# Register your models here.

class BrandAdmin(admin.ModelAdmin):
    pass

class ProductAdmin(admin.ModelAdmin):
    list_filter = ["brand_id"]

admin.site.register(Brand, BrandAdmin)
admin.site.register(Product, ProductAdmin)
