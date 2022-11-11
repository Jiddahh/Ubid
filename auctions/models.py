from turtle import title
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.forms import BooleanField

# from . import forms

class User(AbstractUser):
    pass

class Listing(models.Model):
    CATEGORY_CHOICES = [
    ('fashion', 'Fashion'),
    ('toys', 'Toys'),
    ('electronics', 'Electronics'),
    ('home', 'Home'),
    ('art', 'Art')
]
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=64,blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    image = models.URLField(max_length=250)
    category = models.CharField(max_length=20,blank=True,choices=CATEGORY_CHOICES,default='fashion')
    tag = models.CharField(max_length=10, default='active')
    user = models.CharField(max_length=64)
    date_time = models.DateTimeField(default=timezone.now, blank=True)

    def __str__(self):
        return f"[{self.title} {self.tag} {self.category} {self.description} ${self.price} {self.image} Listed by: {self.user} Created: {self.date_time}]"
    
class Bid(models.Model):
    title = models.CharField(max_length=64, blank=True)
    date_time = models.DateTimeField(default=timezone.now, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.title}, {self.price} bid by {self.user}"

class Comments(models.Model):
    comment = models.TextField(max_length=250)
    user_commented = models.CharField(max_length=64)
    listing = models.CharField(max_length=64)
    user_listing = models.CharField(max_length=64)

class Watchlists(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist", null=True)
    title = models.CharField(max_length=64)
    watchlist = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title}, {self.user}, {self.watchlist}"