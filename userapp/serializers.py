from rest_framework import serializers
from accounts.models import Accounts, Address
from artist.models import Artist,Event
from .models import Booking, Order, Payment


class userSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accounts
        fields = '__all__'


class bookingSerializer(serializers.ModelSerializer):
    artistname = serializers.PrimaryKeyRelatedField(queryset=Artist.objects.all(), required=False)
    eventname = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all(), required=False)

    class Meta:
        model = Booking
        fields = '__all__'


class paymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class orderSerializer(serializers.ModelSerializer):
    artist = serializers.PrimaryKeyRelatedField(queryset=Artist.objects.all(), required=False)
    user = serializers.PrimaryKeyRelatedField(queryset=Accounts.objects.all(), required=False)
    post_image = serializers.ImageField(source='post.image', read_only= True)
    post_baseprice = serializers.CharField(source='post.base_price', read_only= True)
    artist_buyername = serializers.CharField(source='artist_buyer.artistname', read_only= True)
    user_name = serializers.CharField(source='user_buyer.username', read_only= True)
    artist_sellername = serializers.CharField(source='art_seller.artistname', read_only= True)
    # artist_profileimg = serializers.ImageField(source='artist.profile_img', read_only= True)

    class Meta:
        model = Order
        fields = ['id','art_seller','artist_buyer','user_buyer','user','artist','address','post','payment_method','created_at','order_date','total_price','user_name','artist_sellername','artist_buyername','order_status','post_baseprice','post_image']


class addressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'