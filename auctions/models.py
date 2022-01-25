from curses.ascii import NUL
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Max


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=300)
    description = models.CharField(max_length=5000)
    starting_bid = models.IntegerField()
    url = models.URLField(blank=True)
    category = models.CharField(null=True, max_length=5000)
    creater = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="theirlisting")
    status = models.BooleanField(default=True)
    winner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="theirwinning")

    def max_bid(self):
        if Bid.objects.all().filter(listing=self).aggregate(Max('bid')):
            return Bid.objects.all().filter(listing=self).aggregate(Max('bid'))
        else:
            return self.starting_bid
    
    def __str__(self):
        return f"{self.title}: {self.description} - {self.starting_bid}"


class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bid")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bid")
    bid = models.IntegerField(null=True)


class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=5000)

    def __str__(self):
        return f"{self.text}"

class Watchlist(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="watchlist")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")


