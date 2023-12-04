from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image,ImageDraw
# Create your models here.
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
    )
from django.contrib.auth.base_user import BaseUserManager
class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(('Users must have an email address'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)
    

class User(AbstractBaseUser, PermissionsMixin):
    """ Main User config """
    email = models.EmailField(unique=True, verbose_name='Email Address')
    full_name = models.CharField(max_length=256)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    SUPERADMIN = '1'
    USER = '2'
  
    User_type=(
        ('Superadmin','SUPERADMIN'),
        ('User','USER'),
    
    )
    user_type_data = ((SUPERADMIN, "Superadmin"), ('USER','User'))
    user_type = models.CharField( choices=user_type_data, max_length=10,default=1)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [ 'full_name']

    objects = UserManager()

    class Meta:
        db_table = 'user_profile'

    def __str__(self):

        return f'{self.full_name} '

    def has_perm(self, perm, obj=None):
        # User permission
        return True

    def has_module_perms(self, app_label):
        # User permission to view the ap modules
        return True

class HotelOwner(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.TextField()
    mobile = models.CharField(max_length=12, default="")

    def __str__(self):
        return self.user.full_name

class Hotel(models.Model):
    owner = models.ForeignKey(HotelOwner, on_delete=models.CASCADE)
    hotel_name = models.CharField(max_length=100)
    address = models.TextField()
    Number_of_rooms = models.CharField(max_length=100,default="")
  
    def __str__(self):
        return self.hotel_name

class Branch(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    def __str__(self):
        return self.name


