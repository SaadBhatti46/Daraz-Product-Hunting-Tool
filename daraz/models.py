from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    productLink = models.TextField(max_length=200, blank=True)
    sku = models.TextField(max_length=200, blank=True)
    productName = models.TextField(max_length=200, blank=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, blank=True)
    stock = models.IntegerField(blank=True)
    sales = models.IntegerField(blank=True)
    price = models.TextField(max_length=200, blank=True)
    discount = models.TextField(max_length=200, blank=True)
    beforeDiscount = models.TextField(max_length=200, blank=True)
    brand = models.TextField(max_length=200, blank=True)
    image = models.URLField(max_length=200, blank=True)
    sellerName = models.TextField(max_length=200, blank=True)
    sellerRating = models.TextField(max_length=200, blank=True)
    chatRespomse = models.TextField(max_length=200, blank=True)
    # user = models.ManyToManyField(User)
    # tags = models.ManyToManyField(Tag)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(default="staticavator.png",null=True , blank=True)
    auth_token = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.user.username

class Tracking(models.Model):
    user = models.IntegerField(blank=True)
    product = models.IntegerField(blank=True)


# Create your models here.
