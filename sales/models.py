from django.db import models

from products.models import Product
from users.models import User

# Create your models here.

class Sale(models.Model):
    price_sale = models.PositiveIntegerField()
    amount_sale = models.PositiveIntegerField()
    product = models.ForeignKey(Product, verbose_name="sales_product", on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name="sales_user", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user} - {self.date_joined}"
    
    def total_sale(self):
        return self.amount_sale * self.price_sale
    
