from django.db import models

from users.models import User

# Create your models here.

class Supplier(models.Model):
    document = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, verbose_name='suppliers_user', on_delete=models.CASCADE)
    
