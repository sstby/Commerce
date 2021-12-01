from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.models import fields
from django.forms import widgets
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import *
from django import forms

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
        print(form['owner'].value())
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/new_listing.html", {
            "form" : ListingForm(initial={'owner' : request.user.id})
        })

def open_listing(request, id):

    listing = Listing.objects.get(pk=id)
    bids = Bid.objects.filter(listing=id)
    current_bid = listing.price
    print(listing.price)
    if len(bids) > 0:
        current_bid = max([bid.bid for bid in bids])

    #Добавление ставки
    if request.method == 'POST' and 'make_bid' in request.POST:
        bid = request.POST['bid']
        owner = User.objects.get(pk=request.user.id)
        newbid = Bid.objects.create(user=owner, listing=listing, bid=bid)
        newbid.save()
        return HttpResponseRedirect(reverse("open_listing", args=(id,)))
    else:
        
        comments = Comment.objects.filter(listing=id)
        return render(request, "auctions/listing.html", {
                "listing" : listing,
                "bids" : bids,
                "current_bid" : current_bid,
                "comments" : comments
            })

def make_bid(request, bid):
    pass

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
