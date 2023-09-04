import email
from email.policy import default
from pyexpat import model
from unicodedata import category
from unittest.util import _MAX_LENGTH
from django.db import models
from typing import MutableSequence
from django.db.models.deletion import CASCADE
from django.db.models.fields import AutoField, CharField
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.
class Product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=50)
    category = models.CharField(max_length=50, default="")
    subcategory = models.CharField(max_length=50, default="")
    price = models.IntegerField(default=0)
    desc = models.CharField(max_length=300)
    pub_date = models.DateField()
    image = models.ImageField(upload_to='shop/images', default="")

    def __str__(self):
        return self.product_name
    
class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=70)
    email = models.CharField(max_length=70, default="")
    phone = models.CharField(max_length=70, default="")
    desc = models.CharField(max_length=500, default="")
   

    def __str__(self):
        return self.name


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    user= models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    items_json = models.CharField(max_length=5000, default="")
    name = models.CharField(max_length=70, default="")
    address = models.CharField(max_length=111, default="")
    city = models.CharField(max_length=111, default="")
    state = models.CharField(max_length=111, default="")
    zip_code = models.CharField(max_length=111, default="")
    email = models.CharField(max_length=110, default="")
    phone = models.CharField(max_length=70, default="")

    def __str__(self):
        return self.name


class OrderUpdate(models.Model):
    update_id = models.AutoField(primary_key=True)
    user= models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    order_id = models.IntegerField(default="")
    update_desc = models.CharField(max_length=7000, default="")
    timestamp =  models.DateField(default=now) 

    def __str__(self):
        return self.update_desc[0:7]+"...."


class Cartrecord(models.Model):
    cartid=models.AutoField(primary_key=True)
    cart_user=models.ForeignKey(User,on_delete=models.CASCADE)
    json_data=models.CharField(max_length=500,default="0")

    def __str__(self):
        return self.cart_user.username

