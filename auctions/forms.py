from dataclasses import field
from django.forms import ModelForm
from .models import *

# from django import forms

class ListingForm(ModelForm):
    class Meta:
        model = Listing
        exclude = ['tag', 'user', 'date_time']

class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['price']

class CheckForm(ModelForm):
    watchlist = models.BooleanField()

    class Meta:
        model = Watchlists
        exclude = ['title', 'user']

class CommentForm(ModelForm):
    class Meta:
        model = Comments
        fields = ['comment']