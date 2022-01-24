from tkinter.tix import ListNoteBook
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Bid, Comment, Watchlist


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
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


def create(request):
    if request.method == "GET":
        return render(request, "auctions/create.html")
    else:
        R = request.POST
        list = Listing(title=R["title"], description=R["description"], starting_bid= int(R["bid"]), url=R["url"])
        list.save()
        return HttpResponseRedirect(reverse("index"))
    
def list(request, id):
    return render(request, "auctions/list.html", {
        "list": Listing.objects.get(id=id)
    })
    
def watch(request):
    return render(request, "auctions/watch.html", {
        "watchlist": Watchlist.objects.all()
    })

def add_watch(request, id):
    watch = Watchlist(user=request.user, listing=Listing.objects.get(id=id))
    watch.save()
    return HttpResponseRedirect(reverse("watch"))

def delete_watch(request, id):
    watch = Watchlist.objects.filter(user=request.user, listing=Listing.objects.get(id=id)).first()
    watch.delete()
    return HttpResponseRedirect(reverse("watch"))

def add_bid(request, id):
    if request.method == "POST":
        