from django.contrib import admin

# Register your models here.

from .models import FoodItem, Product, Cart, CartItem

admin.site.register(FoodItem)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)