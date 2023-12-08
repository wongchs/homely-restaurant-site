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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ForeignKey('FoodItem', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f'{self.quantity} of {self.item.name}'
    

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    def __str__(self):
        return f'Cart with {self.items.count()} items'