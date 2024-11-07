from django.db import models
from django.contrib.auth.models import PermissionsMixin,AbstractBaseUser, BaseUserManager


class CustomUserManager(BaseUserManager):
    
    def create_user(self, email, name, password=None, **extra_fields):
        if not email:
            raise ValueError('Email must be Vaild')
        
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save()
        
        return user
    
    def create_superuser(self, email, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, name, password, **extra_fields)



class UserAccount(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    DOB = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    
    phone_verified = models.BooleanField(default=False)
    is_data_entry = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name',]
    
    def get_display_name(self):
        # Use a different field or combine first name and last name
        return self.name 
    
    def __str__(self):
        return self.email