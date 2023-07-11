from rest_framework import serializers
from accounts.models import Accounts, Address
from artist.models import Artist,Event
from .models import Booking, Order, Payment


class userSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accounts
        fields = '__all__'


class bookingSerializer(serializers.ModelSerializer):
    artistname_d = serializers.PrimaryKeyRelatedField(queryset=Artist.objects.all(), required=False)
    booking_artist = serializers.PrimaryKeyRelatedField(queryset=Artist.objects.all(), required=False)
    username_d = serializers.PrimaryKeyRelatedField(queryset=Accounts.objects.all(), required=False)
    eventname = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all(), required=False)
    artist_profileimg = serializers.ImageField(source='artist_name.profile_img', read_only= True)
    user_profileimg = serializers.ImageField(source='username.profile_img', read_only= True)
    eventartist_name = serializers.CharField(source='artist_name.artistname', read_only= True)
    user_name = serializers.CharField(source='username.username', read_only= True)
    bookedevent = serializers.CharField(source='eventname.event_name', read_only= True)
    bookedeventdate = serializers.CharField(source='eventname.event_date', read_only= True)
    bookedeventplace = serializers.CharField(source='eventname.event_place', read_only= True)


    class Meta:
        model = Booking
        fields = ['id','artist_name','username','bookingartist','booking_artist','eventname','booking_date',
                  'slot_no','payment_amount','payment_method','artistname_d','username_d','user_name','artist_profileimg',
                  'user_profileimg','bookedevent','bookedeventplace','bookedeventdate','eventartist_name']


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
    artist_profileimg = serializers.ImageField(source='art_seller.profile_img', read_only= True)
    user_profileimg = serializers.ImageField(source='user_buyer.profile_img', read_only= True)

    class Meta:
        model = Order
        fields = ['id','art_seller','artist_buyer','user_buyer','user','artist','address','post','payment_method',
                  'created_at','order_date','total_price','user_name','artist_sellername','artist_buyername',
                  'order_status','post_baseprice','post_image','artist_profileimg','user_profileimg']


class addressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'