from django.db import models

from users.models import User
from categories.models import Category
from suppliers.models import Supplier
# Create your models here.

class Product(models.Model):    
    code = models.CharField(max_length=255)
    name = models.CharField(max_length=50)
    stock = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    status = models.CharField(max_length=10, choices=[('Available', 'Disponible'), ('Disabled', 'No Disponible')])
    user = models.ForeignKey(User, verbose_name="prodcts_user", on_delete=models.CASCADE)
    category = models.ForeignKey(Category, verbose_name="products_category", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.code} - {self.name}"
    
    def total_product(self):
        return self.stock * self.price
    
