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

    class Meta:
        model = Order
        fields = '__all__'


class addressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'