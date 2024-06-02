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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, verbose_name="products_category", on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, verbose_name="products_supplier", on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date_joined']
    
    def __str__(self):
        return f"{self.code} - {self.name} - {self.user}"
    
    def total_product(self):
        return self.stock * self.price
    
