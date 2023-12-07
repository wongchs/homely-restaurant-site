from django.contrib import admin

# Register your models here.

from .models import FoodItem, Product

admin.site.register(FoodItem)

admin.site.register(Product)