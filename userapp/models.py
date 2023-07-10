from django.db import models
from accounts.models import Accounts, Address
from artist.models import Artist, Post ,Event

# Create your models here.


class Order(models.Model):
    user_buyer = models.ForeignKey(Accounts,on_delete=models.CASCADE,null=True)
    art_seller = models.ForeignKey(Artist,on_delete=models.CASCADE,related_name='art_seller')
    artist_buyer = models.ForeignKey(Artist,on_delete=models.CASCADE,related_name='artist_buyer',null=True)
    address = models.ForeignKey(Address,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE) 
    total_price = models.FloatField(null=True)
    order_date = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(max_length=100,default ='Placed')
    created_at = models.DateTimeField(auto_now_add=True )
    updated_at = models.DateTimeField(auto_now_add=True )
    payment_method = models.CharField(max_length=100,default=True)
   

class Booking(models.Model):
    username = models.ForeignKey(Accounts,on_delete=models.CASCADE,null=True)
    artist_name = models.ForeignKey(Artist,on_delete=models.CASCADE,related_name='artist_name',null=True)
    bookingartist = models.ForeignKey(Artist,on_delete=models.CASCADE,related_name='bookingartist',null=True)
    eventname = models.ForeignKey(Event,on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True,null=True)
    slot_no = models.IntegerField(null=True)
    payment_amount = models.FloatField(null=True)
    payment_method = models.CharField(max_length=100,default='razorpay')
    

class Payment(models.Model):
    # payment_type = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
#     payment_time = models.DateTimeField(auto_now_add=True)

