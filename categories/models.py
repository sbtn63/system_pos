from django.db import models

from users.models import User

# Create your models here.

class Category(models.Model):
    code = models.PositiveIntegerField()
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=50, blank=True, null=True)
    user = models.ForeignKey(User, verbose_name="categories_user", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.code} - {self.name}"