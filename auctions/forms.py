from dataclasses import field
from django.forms import ModelForm
from .models import *
from django import forms

# from django import forms

class ListingForm(ModelForm):
    class Meta:
        model = Listing
        exclude = ['tag', 'user', 'date_time']

class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['price']

# class CheckForm(ModelForm):
#     # watchlist = forms.DecimalField(widget=forms.CheckboxInput(attrs={"value":"watchlist"}))
#     class Meta:
#         model = Watchlists
#         fields = ['watchlist']

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']