from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Debes tener un correo electronico")
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        
        return user
    
    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        return self._create_user(email, password, **extra_fields)
    
    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        
        return self._create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(max_length=100, unique=True)
    rol = models.CharField(max_length=50, choices=[('Admin', 'Admin'), ('Employee', 'Employee')], default='Admin')
    created_by_user = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    
    date_joined = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    objects = CustomUserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    

    def fullname(self):
        return f'{self.first_name} {self.last_name}'    
    

class Dashboard(models.Model):
    name_company = models.CharField(max_length=50)
    logo_company = models.ImageField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


@receiver(post_save, sender=User)
def add_user_to_group(sender, instance, created, **kwargs):
    if created and instance.rol == 'Admin':
        dashboard = Dashboard.objects.create(name_company=instance.email, user=instance)
        dashboard.save()