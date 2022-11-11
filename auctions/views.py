from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import urllib.parse

from django.contrib.auth.decorators import login_required

from django.contrib import messages

from .models import *
from .forms import *


def index(request):
    active_listings = Listing.objects.all().filter(tag="active")
    return render(request, "auctions/index.html", {
        "active_listings": active_listings
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def create_listing(request):

    if request.user.is_authenticated:
        username = request.user.get_username()
        
    forms = ListingForm()

    if request.method == 'POST':
        listing = Listing(user=username)
        forms = ListingForm(request.POST, request.FILES, instance=listing)
        if forms.is_valid():
            listing = forms.save()
            return HttpResponseRedirect(reverse("index"))

        return render(request, "auctions/create_listing.html" , {
            "message": "Title, Starting bid, and Image URL must be provided",
            "form": forms
        })
    
    return render(request, "auctions/create_listing.html", {
        "form": forms
    })

@login_required
def listing(request, title):
    checkbox = CheckForm()
    form = BidForm()

    listing = Listing.objects.all().filter(title=title).first()
    title = listing.title
    user = listing.user

    if request.user.is_authenticated:
        username = request.user.get_username()
    
    bids = Bid.objects.all().filter(title=title).values_list("price", flat=True)
    max_bid = max(bids)
    

    if request.method == "POST":
        watchlist = CheckForm(request.POST)
        bid = Bid(title=title, user=username)
        bidform = BidForm(request.POST, request.FILES, instance=bid)
        
        if watchlist.is_valid():
            if "watchlist" in request.POST:
                watchlist_data = Watchlists.objects.all().filter(title=title, user=username).first()

                if watchlist_data:
                    watchlist_data.delete()
                else:
                    true_wtchlist = Watchlists.objects.create(title=title, user=username)

        if bidform.is_valid():
            price = bid.price
            if not bids:
                bid = bidform.save()
                return render(request, "auctions/listing.html", {
                        "message": "Your bid has been placed succesfully",
                        "form": form,
                        "listing": listing,
                        "checkbox": checkbox
                    })
            else:
                max_bid = max(bids)
                if price >= listing.price and price > max_bid:
                    bid = bidform.save()
                    return render(request, "auctions/listing.html", {
                        "message": "Bid price must be equal or greater than starting price and higher than highest bid",
                        "form": form,
                        "listing": listing,
                        "checkbox": checkbox,
                        "max_bid": max_bid

                    })
                else:
                    return render(request, "auctions/listing.html", {
                        "message": "Bid price must be equal or greater than starting price and higher than highest bid",
                        "form": form,
                        "listing": listing,
                        "checkbox": checkbox,
                        "max_bid": max_bid

                    })
            
    if request.GET.get('close') == 'close':
        bid = Bid.objects.all().filter(title=title, price=max_bid).first()
        max_bid_user = bid.user

        listing.tag = 'closed'
        listing.save()

        if username == max_bid_user:
            return render(request, "auctions/listing.html", {
                "message": "Thank you for your entry into this auction. You have emerged the winner and this listing has been closed"
            })
        
    return render(request, "auctions/listing.html", {
        "form": form,
        "listing": listing,
        "checkbox": checkbox,
        "max_bid": max_bid,
        "user": user
    })


