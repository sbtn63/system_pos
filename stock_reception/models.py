from django.db import models

from products.models import Product
from suppliers.models import Supplier
from users.models import User

class StockReception(models.Model):
    quantity_received = models.PositiveIntegerField()
    unit_price = models.PositiveIntegerField()
    reception_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    note = models.CharField(max_length=50, blank=True, null=True)
    product = models.ForeignKey(Product, verbose_name="stock_receptions_product", on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name="stock_receptions_user", on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, verbose_name="stock_receptions_supplier", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)