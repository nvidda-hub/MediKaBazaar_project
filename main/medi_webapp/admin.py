from django.contrib import admin
from medi_webapp.models import Product
# Register your models here.


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'product_name', 'price','quantity']
