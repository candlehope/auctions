from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime



CATAGORIES = [ ('clothing', 'Clothing'), ('furniture','Furniture'), ('auto', 'Auto'), ('electronics','Electronics'), ("games_&_toys", 'Games & Toys'), ('appliances','Appliances'), ('books','Books'), ]

class User(AbstractUser):
    pass

class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    catagory = models.CharField(max_length=14, choices=CATAGORIES)
    title = models.CharField(max_length=32, blank=False)
    description = models.CharField(max_length=250, blank=True)
    price = models.IntegerField(blank=False)
    image_URL = models.CharField(max_length=512, blank=True)
    date = datetime.now()

    def __str__(self):
        return f"{self.user}: posted {self.title} to {self.catagory} as {self.description} for {self.price}"

class Bid(models.Model):   
    user = models.ManyToManyField(User, related_name="bidder")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    amount = models.IntegerField(blank=False)

class Comment(models.Model):
    user = models.ManyToManyField(User, related_name="poster")
    listing = models.ManyToManyField(Listing, blank=False, related_name="post")
    body = models.CharField(max_length=250, blank=False)