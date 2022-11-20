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

        messages.warning(request, 'Title, Image URL, and Starting price must be provided')
        return HttpResponseRedirect(reverse("create_listing"))
    
    return render(request, "auctions/create_listing.html", {
        "form": forms
    })

@login_required
def listing(request, title):
    if request.user.is_authenticated:
        username = request.user.get_username()

    form = BidForm()
    comment_form = CommentForm()

    listing_object = Listing.objects.all().filter(title=title).first()
    author = listing_object.user
    
    bids = Bid.objects.all().filter(title=title).values_list("price", flat=True)
    max_bid = max(bids, default=0)
    comments = Comment.objects.all().filter(list_title=title)
    
    watchlist_data = Watchlists.objects.all().filter(title=title, user=username).first()


    if request.method == "POST":
        bid = Bid(title=title, user=username)
        bidform = BidForm(request.POST, request.FILES, instance=bid)
        
        if "watchlist" in request.POST:
            if not watchlist_data:
                watchlisted = Watchlists.objects.create(title=title, user=username, watchlist='True')
                watchlisted.save()
            if watchlist_data:
                watchlist_data.delete()
                
            return HttpResponseRedirect(reverse('listing', args=(), kwargs={'title': title}))
                

        if "price" in request.POST:
            if bidform.is_valid():
                price = bid.price
                if not bids:
                    bid = bidform.save()
                    messages.success(request, 'Your bid has been placed succesfully')
                    return HttpResponseRedirect(reverse('listing', args=(), kwargs={'title': title}))
                    
                else:
                    max_bid = max(bids)
                    if price >= listing_object.price and price > max_bid:
                        bid = bidform.save()
                        messages.success(request, 'Your bid has been placed succesfully')
                        return HttpResponseRedirect(reverse('listing', args=(), kwargs={'title': title}))
                        
                    else:
                        messages.warning(request, 'Bid price must be greater than highest bid and starting price')
                        return HttpResponseRedirect(reverse('listing', args=(), kwargs={'title': title}))
                        
            
        if "close" in request.POST:
            bid = Bid.objects.all().filter(title=title, price=max_bid).first()
            max_bid_user = bid.user

            listing_object.tag = 'closed'
            listing_object.save()

            if username == max_bid_user:
                messages.warning(request, 'Thank you for your entry into this auction. You have emerged the winner and this listing has been closed')
                return HttpResponseRedirect(reverse('listing', args=(), kwargs={'title': title}))
                


        comment = Comment(user_commented=username, list_title=title, list_author=author)
        comment_form = CommentForm(request.POST, request.FILES, instance=comment)
        if "comment" in request.POST:
            if comment_form.is_valid():
                user_comment = comment_form.save()
                comments = Comment.objects.all().filter(list_title=title)
                return HttpResponseRedirect(reverse('listing', args=(), kwargs={'title': title}))
                

    return render(request, "auctions/listing.html", {
        "form": form,
        "listing": listing_object,
        "max_bid": max_bid,
        "users": author,
        "commentform": comment_form,
        "comments": comments,
        "watchlist_data": watchlist_data

    })


def categories(request):
    categories = [c[0] for c in Listing.category.field.choices]

    for category in categories:
        active_listings = Listing.objects.all().filter(tag='active', category=category)

        for active_listing in active_listings:
            if active_listing in request.GET:
                title = active_listing.title
                return HttpResponseRedirect(reverse('listing', args=(), kwargs={'title': title}))
            else:
                pass
    return render(request, "auctions/categories.html", {
        "categories": categories
    })

def category(request):
    category = request.GET.get("name")
    active_listings = Listing.objects.all().filter(tag='active', category=category)

    return render(request, "auctions/category.html", {
        "active_listings": active_listings,
        "category": category
    })

@login_required
def watchlist(request):
    if request.user.is_authenticated:
        username = request.user.get_username()

    watchlist_data = Watchlists.objects.all().filter(user=username)
    active_listings = []

    for watchlist in watchlist_data:
        active_listing = Listing.objects.all().filter(title=watchlist.title).first()
        active_listings.append(active_listing)


    return render(request, "auctions/watchlist.html", {
        "active_listings": active_listings
    })