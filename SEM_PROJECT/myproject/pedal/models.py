from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from .managers import CustomUserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
# class AppUser(AbstractUser, PermissionsMixin):
#     #username=None
#     bits_id=models.CharField(unique=True,max_length=50)
#     profile_img    = models.ImageField(upload_to='images/Users/', null=True, blank=True, default=None)
#     # first_name = models.CharField(_("first_name"),max_length=50)
#     # last_name =  models.CharField(_("last_name"),max_length=50)
#     email = models.EmailField(_("email address"), unique=True)
#     phone = models.CharField(max_length=15)
#     address =  models.CharField(max_length=100)
    
#     USERNAME_FIELD = "email"
#     REQUIRED_FIELDS = []
#     objects = CustomUserManager()
    

class AppUser(models.Model):
   #bits_id=models.CharField(unique=True,max_length=50)
   profile_img    = models.ImageField(upload_to='images/Users/', null=True, blank=True, default=None)
   #first_name = models.CharField(_("first_name"),max_length=50)
   #last_name =  models.CharField(_("last_name"),max_length=50)
   #email = models.EmailField(_("email address"), unique=True)
   address =  models.CharField(max_length=100)
   phone = models.CharField(max_length=15)
   authUser=models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)

class Cycle(models.Model):
   cycle_img    = models.ImageField(null=True, blank=True, upload_to="images/")
   owner =models.ForeignKey(AppUser, blank=True, null=True, on_delete=models.SET_NULL,related_name='current_owner')
   dop = models.DateTimeField('Date of Purchase')
   model = models.CharField(max_length=50)
   price=models.IntegerField()
   lend_or_sell = models.CharField(max_length=50)
   description = models.CharField(max_length=5000)
   is_avail=models.BooleanField(default=True)
   is_sold=models.BooleanField(default=False)
   is_being_rented=models.BooleanField(default=False)
   end_time=models.DateTimeField(default=datetime.now())
   description = models.CharField(max_length=5000,null=True, blank=True)
   no_of_rents = models.IntegerField(default=0)
   total_stars=models.IntegerField(default=0)
   sold_to =models.ForeignKey(AppUser,default=None, blank=True, null=True, on_delete=models.SET_NULL,related_name='cycle_buyer')

   #Cycle(model='hero Razor back',address='1102 MSA 1 ',dop='06/09/19',price='190',img='cycle2.jpg')

class Order(models.Model):
   razorpay_order_id=models.CharField(unique=True,max_length=50)
   payment_staus=models.CharField(max_length=50)
   user =models.ForeignKey(AppUser, blank=True, null=True, on_delete=models.SET_NULL)
   cycle =models.ForeignKey(Cycle, blank=True, null=True, on_delete=models.SET_NULL)
   amount = models.IntegerField(default=0)

class Payment(models.Model):
   razorpay_payment_id=models.CharField(unique=True,max_length=50)
   razorpay_order_id=models.CharField(unique=True,max_length=50)
   razorpay_signature=models.CharField(max_length=1000)
   amount = models.IntegerField(default=0)
   # payment_staus=models.CharField(max_length=50)
   # user =models.ForeignKey(AppUser, blank=True, null=True, on_delete=models.SET_NULL)
   # cycle =models.ForeignKey(Cycle, blank=True, null=True, on_delete=models.SET_NULL)
   
class Rent(models.Model):
   payment=models.ForeignKey(Payment, blank=True, null=True, on_delete=models.SET_NULL)
   #order=models.ForeignKey(Order, blank=True, null=True, on_delete=models.SET_NULL)
   user =models.ForeignKey(AppUser, blank=True, null=True, on_delete=models.SET_NULL)
   cycle =models.ForeignKey(Cycle, blank=True, null=True, on_delete=models.SET_NULL)
   start_time=models.DateTimeField()
   end_time=models.DateTimeField()
   is_avail=models.BooleanField(default=True)
   

class Transaction(models.Model):
   payment=models.ForeignKey(Payment, blank=True, null=True, on_delete=models.SET_NULL)
   user =models.ForeignKey(AppUser, blank=True, null=True, on_delete=models.SET_NULL,related_name='first_party')
   cycle =models.ForeignKey(Cycle, blank=True, null=True, on_delete=models.SET_NULL)
   transaction_with =models.ForeignKey(AppUser, blank=True, null=True, on_delete=models.SET_NULL,related_name='other_party')
   transaction_time=models.DateTimeField(default=datetime.now())
   transaction_name=models.CharField(max_length=50)
   