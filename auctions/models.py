from turtle import title
from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime

# from . import forms

class User(AbstractUser):
    pass

class Listings(models.Model):
    CATEGORY_CHOICES = [
    ('fashion', 'Fashion'),
    ('toys', 'Toys'),
    ('electronics', 'Electronics'),
    ('home', 'Home'),
    ('art', 'Art')
]
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=250,blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    image = models.URLField(max_length=250)
    category = models.CharField(max_length=20,blank=True,choices=CATEGORY_CHOICES,default='fashion')
    tag = models.CharField(max_length=10)
    user = models.CharField(max_length=64)

    # def __str__(self):
    #     return f"{self.title} 
        # {self.tag} {self.category}
        # {self.description} 
        # ${self.price} 
        # {self.image}  
        # Listed by: {self.user}"
    
class Bid(models.Model):
    date_time = models.DateTimeField(default=datetime.now, blank=True)
    bid_price = models.DecimalField(max_digits=4, decimal_places=2)
    user = models.CharField(max_length=64)

class Comments(models.Model):
    comment = models.CharField(max_length=250)
    user_commented = models.CharField(max_length=64)
    listing = models.CharField(max_length=64)
    user_listing = models.CharField(max_length=64)

    