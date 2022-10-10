from dataclasses import field
from django.forms import ModelForm
from .models import Listings

# from django import forms

class ListingForm(ModelForm):
    class Meta:
        model = Listings
        exclude = ['tag', 'user']