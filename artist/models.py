from django.db import models
from cloudinary.models import CloudinaryField


# Create your models here.

class Artist(models.Model):
    full_name = models.CharField(max_length=100)
    artistname = models.CharField(max_length=15,unique=True)
    password = models.CharField(max_length=100)
    email = models.CharField(max_length=30,unique=True)
    profile_img = models.ImageField(upload_to='profiles', null=True)
    phone_number = models.CharField(max_length=13)
    place = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now_add=True,null=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    from_google = models.BooleanField(default=False)



class Post(models.Model):
    art_content = models.CharField(max_length=150)
    image = models.ImageField(upload_to='posts', null=False)
    base_price = models.FloatField(null=False)
    shipping_price = models.FloatField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    artist = models.ForeignKey(Artist,on_delete=models.CASCADE)



class Event(models.Model):
    event_name = models.CharField(max_length=100,unique=True)
    event_date = models.DateField()
    event_place = models.CharField(max_length=100)
    event_start_time = models.TimeField(auto_now=False, auto_now_add=False)
    event_end_time = models.TimeField(auto_now=False, auto_now_add=False)
    total_slots = models.IntegerField(blank=True,null=True)
    conducting_artist = models.ForeignKey(Artist,on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)
    booking_price = models.FloatField(default=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)