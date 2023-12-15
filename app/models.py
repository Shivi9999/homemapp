from django.db import models
# Create your models here.
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
    )
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth import get_user_model

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
    username = models.CharField(max_length=256)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    SUPERADMIN = '1'
    USER = '2'
    Web_USER = '3'
  
    User_type=(
        ('Superadmin','SUPERADMIN'),
        ('User','USER'),
        ('Web_user','Web_USER'),
    
    )
    user_type_data = ((SUPERADMIN, "Superadmin"), (USER,"User"),(Web_USER,"Web_user"))
    user_type = models.CharField( choices=user_type_data, max_length=10,default='Superadmin')
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [ 'username']

    objects = UserManager()

    class Meta:
        db_table = 'user_profile'

    def __str__(self):

        return f'{self.username} '

    def has_perm(self, perm, obj=None):
        # User permission
        return True

    def has_module_perms(self, app_label):
        # User permission to view the ap modules
        return True



class PropertyOwner(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property_name = models.CharField(max_length=120)
    address = models.TextField()
    mobile = models.CharField(max_length=12 )

    def __str__(self):
        return self.property_name


class QuestionAnswer(models.Model):
    
    question = models.CharField(max_length=500)
    answer=models.CharField(max_length=2000)
    

    def __str__(self):
        return self.question


class Notification(models.Model):
    users = models.ManyToManyField(User)
    title = models.CharField(max_length=255)
    message = models.CharField(max_length=2550)
    
    def __str__(self):
        return self.title


class TermsCondition(models.Model):
    
    terms_condition = models.TextField()
   
   
    def __str__(self):
        return self.terms_condition


class PrivacyPolicy(models.Model):
    
    privacy_policy = models.TextField()
    

    def __str__(self):
        return self.privacy_policy


class Faq(models.Model):
    question=models.CharField(max_length=500)
    answer=models.CharField(max_length=2000)
    def __str__(self):
        return self.question



class Add_user(models.Model):
    user=models.OneToOneField("User", verbose_name=("add_users"), on_delete=models.CASCADE)
    address=models.CharField( max_length=50)
    mobile=models.CharField(max_length=12)
    user_image=models.ImageField(upload_to='user_img', max_length=100)
    def __str__(self):
        return self.user.username



class Add_hotel(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    property_name = models.CharField(max_length=50)
    total_room = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    mobile = models.CharField(max_length=12)
    flat_image = models.ImageField(upload_to='flat_img', max_length=100)

    def __str__(self):
        return self.property_name



