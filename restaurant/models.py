from django.db import models
from django.conf import settings

class FoodItem(models.Model):
    type = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='menu_items/')
    details_url = models.URLField(blank=True, null=True)
    
    def __str__(self):
        return f'{self.type} - {self.name}'

class Product(models.Model):
    type = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='product_images/')
    details_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f'{self.type} - {self.name}'
    
class CartItem(models.Model):
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE)
    item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=6, decimal_places=2)  # Add a price field

    def __str__(self):
        return f'{self.quantity} x {self.item.name}'

    def subtotal(self):
        return self.quantity * self.price
    
class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart {self.id}"
