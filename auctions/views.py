from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .forms import ListingForm
from .models import User, Listing
from django.contrib import messages


def index(request):
        listings = Listing.objects.all()
        return render(request, "auctions/index.html", {"listing": listings, "errors": form.errors})
    return render(request, "auctions/index.html", {"listing": listings})


def new_listing(request):
    auction_form = ListingForm()
    return render(request, "auctions/create_listing.html", {"auction_form": auction_form})

def create_listing(request):
    if request.method == "POST":
        updated_form = request.POST.copy()
        updated_form.update({'user': request.user})
        form = ListingForm(updated_form)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("index"))
        else: 
            messages.error(request, form.errors)
            return HttpResponseRedirect(reverse("new"))
    
        


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user:
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
