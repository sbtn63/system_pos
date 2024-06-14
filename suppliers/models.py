from django.db import models

from users.models import User

# Create your models here.

class Supplier(models.Model):
    document = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=50)
    user = models.ForeignKey(User, verbose_name='suppliers_user', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.name}'
    
    
