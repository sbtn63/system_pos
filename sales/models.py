from django.db import models

from products.models import Product
from users.models import User

# Create your models here.

class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price_sale = models.PositiveIntegerField()
    amount_sale = models.PositiveIntegerField()
    date_joined = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date_joined']
    
    def __str__(self):
        return f"{self.user} - {self.date_joined}"
    
    def total_sale(self):
        return self.amount_sale * self.price_sale
    
