from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    category = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.category}"

class Listing(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    photo = models.ImageField(upload_to="images", default="images/no_photo.png")
    price = models.DecimalField(decimal_places=2, max_digits=20)

    @property
    def photo_url(self):
        if self.photo and hasattr(self.photo, 'url'):
            return self.photo.url

class Bid(models.Model):
    bid_by_user = models.ForeignKey(User, on_delete=models.CASCADE)
    bid_bid = models.DecimalField(decimal_places=2, max_digits=20)
    bid_listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

class Comment(models.Model):
    comment_by_user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    comment_text = models.TextField()
    comment_date = models.DateTimeField(auto_now=True)