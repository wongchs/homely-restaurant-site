from django.db import models

class FoodItem(models.Model):
    type = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='menu_items/')
    details_url = models.URLField(blank=True, null=True)
    
    def __str__(self):
        return f'{self.type} - {self.name}'