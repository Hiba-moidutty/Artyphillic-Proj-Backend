from rest_framework import serializers
from artist.models import Artist,Event, Post


class artistSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(required=False)
    password = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    phone_number = serializers.CharField(required=False)
    place = serializers.CharField(required=False)
    artistname = serializers.CharField(required=False)

    class Meta:
        model=Artist
        fields='__all__'


class postSerializer(serializers.ModelSerializer):
    artist_name = serializers.CharField(source='artist.artistname', read_only= True)
    artist_id = serializers.CharField(source='artist.id', read_only= True)
    artist_profileimg = serializers.ImageField(source='artist.profile_img', read_only= True)
    
    class Meta:
        model=Post
        fields=['id','art_content','image','base_price','shipping_price','artist_name','artist','artist_id','artist_profileimg' ]
        # fields='__all__'


class eventSerializer(serializers.ModelSerializer):
    artist_id = serializers.CharField(source='conducting_artist.id', read_only= True)
    artist_name = serializers.CharField(source='conducting_artist.artistname', read_only= True)
    artist_profileimg = serializers.ImageField(source='conducting_artist.profile_img', read_only= True)

    class Meta:
        model=Event
        fields=['id','event_name','event_date','event_start_time','event_end_time','total_slots','event_place','artist_name',
                'conducting_artist','artist_id','artist_profileimg','booking_price','is_available']
        # fields='__all__'
