from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.models import fields
from django.forms import widgets
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import *
from django import forms
from django.contrib.auth.decorators import login_required

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ('title', 'description', 'category','price','photo','owner')
        widgets = {
            'owner' : widgets.HiddenInput()
        }

def index(request):
    return render(request, "auctions/index.html",{
        'listings' : Listing.objects.all()
    })

def new_listing(request):
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        
        print(form.errors)
        if form.is_valid():
            
            form.save()
        else:
            print('form not valid')
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/new_listing.html", {
            "form" : ListingForm(initial={'owner' : request.user.id})
        })

def open_listing(request, id):
    print(request.POST)
    listing = Listing.objects.get(pk=id)
    bids = Bid.objects.filter(listing=id)
    current_bid = listing.price
    watchlist = Watchlist.objects.all().filter(user_id=request.user.id, listings=listing)
    if len(watchlist) > 0:
        in_watchlist = True
    else:
        in_watchlist = False
    if len(bids) > 0:
        current_bid = max([bid.bid for bid in bids])
    winner = None
    if listing.state == False:
        winner_bid = Bid.objects.get(bid = current_bid)
        winner = winner_bid.user_id
    
    #Добавление ставки
    if request.method == 'POST' and 'make_bid' in request.POST:
        bid = request.POST['bid']
        owner = User.objects.get(pk=request.user.id)
        newbid = Bid.objects.create(user=owner, listing=listing, bid=bid)
        newbid.save()
        return HttpResponseRedirect(reverse("open_listing", args=(id,)))
    elif request.method == 'POST' and 'make_comment' in request.POST:
        text = request.POST['comment']
        by_user = User.objects.get(pk=request.user.id)
        new_comment = Comment.objects.create(by_user=by_user, listing=listing, text=text)
        new_comment.save()
        return HttpResponseRedirect(reverse("open_listing", args=(id,)))
    else: 
        comments = Comment.objects.filter(listing=id)
        return render(request, "auctions/listing.html", {
                "listing" : listing,
                "bids" : bids,
                "current_bid" : current_bid,
                "comments" : comments,
                "in_watchlist" : in_watchlist,
                "winner" : winner
            })

def watchlist(request):
    user = User.objects.get(pk=request.user.id)
    print(user)
    user_watchlist = Watchlist.objects.get(user=user)
    watchlist = user_watchlist.listings.all()
    return render(request, "auctions/watchlist.html",{
        "listings" : watchlist
    })

def categories(request):
    cats = Category.objects.all()
    return render(request, "auctions/categories.html",{
        'categories' : cats
    })
def open_category(request, cat):
    category = Category.objects.get(category=cat)
    listings = Listing.objects.all().filter(category=category)
    return render(request, "auctions/open_category.html",{
        'listings' : listings,
        'cat_name' : category.category
    })

@login_required
def add_to_watchlist(request, id):
    user = User.objects.get(pk=request.user.id)
    listing = Listing.objects.get(pk=id)
    user_watchlist = Watchlist.objects.all().filter(user=user)
    if len(user_watchlist) > 0:
        new_listing_to_watchlist = Watchlist.objects.get(user=user)
        new_listing_to_watchlist.listings.add(listing)
    else:
        new_watchlist = Watchlist.objects.create(user=user)
        new_watchlist.save()
        new_listing_to_watchlist = Watchlist.objects.get(user=user)
        new_listing_to_watchlist.listings.add(listing)
    return HttpResponseRedirect(reverse("open_listing", args=(id,)))

def remove_form_watchlist(request, id):
    user = User.objects.get(pk=request.user.id)
    listing = Listing.objects.get(pk=id)
    user_watchlist = Watchlist.objects.get(user=user)
    user_watchlist.listings.remove(listing)
    return HttpResponseRedirect(reverse("open_listing", args=(id,)))

def close_auction(request, id):
    listing = Listing.objects.get(pk=id)
    listing.state = False
    listing.save()
    return HttpResponseRedirect(reverse("open_listing", args=(id,)))

def login_view(request, query=None):
    if request.method == "POST":
        print(query)
        
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
        print(query)
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
