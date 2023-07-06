from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import status
from accounts.models import Address
from artist.serializers import artistSerializer, eventSerializer, postSerializer
from drf_spectacular.utils import extend_schema
import cloudinary.uploader 
from django.contrib.auth import authenticate
from userapp.models import Booking, Order
from userapp.serializers import addressSerializer, bookingSerializer, orderSerializer, paymentSerializer
from . authentication import encode_password, verify_password, create_jwt_token
from .models import Artist, Post ,Event
# Create your views here.


class artistSignUp(APIView):
    def post(self,request):
        data = request.data
        try:
            full_name = data['full_name']
            artistname = data['artistname']
            email = data['email']
            password = data['password']
            phone_number = data['phone_number']
            # place = data['place']
        except:
            return Response({'status': 'Please give all details'})
        
        check_artist  = Artist.objects.all()
        for a in check_artist:
            if a.email == email:
                return Response({'status': 'Email already Exists'})
            elif a.artistname == artistname:
                return Response({'status': 'Username already Exist'})
            elif a.phone_number == phone_number:
                return Response({'status': 'Phone Number already Exist'})
        password=encode_password(data['password'])
        profile_image = "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png"
        upload_result = cloudinary.uploader.upload(
                    profile_image,
                    folder='profiles'
                )
        print("success")
        artist =  Artist.objects.create(
            full_name=full_name,artistname=artistname,
            email=email,password=password,
            phone_number=phone_number,
             profile_img=profile_image
        )
        artist.save()
        serializer = artistSerializer(artist,many=False)
        return Response(serializer.data) 	
        # return Response({'status' : 'Success'})


@extend_schema(responses=artistSerializer)
@api_view(['POST'])
def artist_Login(request):
    email = request.data['email']
    password = request.data['password']
    if not email or not password:
        return Response({'status' : 'Please provide details(email,password)'})
    try:
        artist = Artist.objects.filter(email=email).first()
    except Exception as e:
        print(e)
    check = False
    if artist:
        check = verify_password(password,artist.password)
    else:
        raise exceptions.APIException("password is incorrect")
    token = create_jwt_token(artist.id)
    data = {
                'id':artist.id,
                'name':artist.artistname,
                'email':artist.email,
                'password':artist.password,
                'token':token,
                'role':'artist'
                }
    return Response(data=data, status=status.HTTP_200_OK)


@extend_schema(responses=artistSerializer)
@api_view(['POST'])
def google_artistLogin(request):
    email = request.data['email']

    try:
        artist = Artist.objects.filter(email=email).first()
        if artist:
            print("inside the try function")
            if artist.is_blocked:
                return Response({'status': 'this Artist is Blocked'}) 
            token = create_jwt_token(artist.id)
            data = {
                'id':artist.id,
                'name':artist.full_name,
                'email':artist.email,
                'token':token,
                'role':'artist'
                }
            return Response(data=data, status=status.HTTP_200_OK)
        else:
            name = request.data['name']
            email = request.data['email']
            print("google details fetched success..........")
            artist = Artist.objects.create(
                full_name=name,
                artistname=name,
                email=email,
                from_google=True
            )
            artist.save()
            namesss=artist.full_name
            print(namesss,'okkkkkkkkkkkkkkkkk')
            serializer = artistSerializer(artist,many=False)
            n_artist = Artist.objects.filter(email=email).first()
            if n_artist.is_blocked:
                return Response({'status': 'This Artist is Blocked'}) 
            token = create_jwt_token(n_artist.id)
            data = {
                'id':n_artist.id,
                'name':n_artist.full_name,
                'email':n_artist.email,
                'token':token,
                'role':'artist',
                }
            return Response(data=data, status=status.HTTP_200_OK)
        
    except Exception as e:
        print(e)
            


@extend_schema(responses=artistSerializer(many=True))
@api_view(['GET'])
def artist_profile(request,id):
    try:
        artist = Artist.objects.get(id=id)
        serializer = artistSerializer(artist,many=False)
        artist_details = serializer.data
        return Response({'data': artist_details}, status=status.HTTP_200_OK)
    except Artist.DoesNotExist:
        return Response({'error': 'Artist not found'}, status=status.HTTP_404_NOT_FOUND)



@extend_schema(responses=artistSerializer)
@api_view(['PATCH'])
def artist_profile_update(request,id):
    try:
        artist = Artist.objects.get(id=id)
        serializer = artistSerializer(artist,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("Profile updated Successfully")
        else:
            print(serializer.errors,'erroooooooorssssss')
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Artist.DoesNotExist:
        return Response("Artist not found", status=status.HTTP_404_NOT_FOUND )
    

@api_view(['POST'])
def addProfilePic(request, artist_id):
    artist = Artist.objects.get(id=artist_id)   # Assuming the artist is authenticated
    profile_picture = request.FILES["profile_img"]
    if profile_picture:
        upload_result = cloudinary.uploader.upload(
            profile_picture,
            folder='profiles'
        )
        print(upload_result, 'lllllllllllllll')
        profile_picture_url = upload_result['secure_url']
       # Update the profile_img field with the image URL
        artist.profile_img = profile_picture_url
        artist.save()
        return Response({"profile_picture_url": profile_picture_url})
    else:
        return Response({"message": "Unsuccessful"})



@extend_schema(responses=postSerializer)
@api_view(['POST'])
def create_posts(request):
    serializer = postSerializer(data=request.data)
    if serializer.is_valid():
        image = serializer.validated_data['image']
        if image:
            upload_result = cloudinary.uploader.upload(
                image,
                folder='posts'
            )
        image_url = upload_result['secure_url']
        serializer.validated_data['image'] = image_url
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(responses=postSerializer(many=True))
@api_view(['GET'])
def artistpost_list(request, artist_id):
    posts = Post.objects.filter(artist_id=artist_id).order_by('-created_at')
    print(posts,'artist posts')
    serializer = postSerializer(posts, many=True)
    return Response({'data':serializer.data}, status=status.HTTP_200_OK)


@extend_schema(responses=eventSerializer(many=True))
@api_view(['GET'])
def artistevent_list(request, artist_id):
    events = Event.objects.filter(conducting_artist=artist_id).order_by('-created_at')
    print(events,'artist events')
    serializer = eventSerializer(events, many=True)
    return Response({'data':serializer.data}, status=status.HTTP_200_OK)



@extend_schema(responses=postSerializer)
@api_view(['GET'])
def post_list(request):
    posts = Post.objects.all().order_by('-updated_at')
    serialized_posts = []
    
    for post in posts:
        post_data = postSerializer(post).data
        post_data['artist_name'] = post.artist.artistname  # Fetch the artist's username
          # Add the artist's username to the serialized post data
        post_data['artist_id'] = post.artist.id  # Fetch the artist's id
        profile_image = post.artist.profile_img  # Fetch the artist's profileimg
        if profile_image:
            post_data['artist_profileimg'] = profile_image.url
        else:
            post_data['artist_profileimg'] = None
        serialized_posts.append(post_data)
    
    return Response(serialized_posts, status=status.HTTP_200_OK)



@extend_schema(responses=postSerializer)
@api_view(['PATCH'])
def edit_post(request,postid):
    post = Post.objects.get(id=postid)
    serializer = postSerializer(post,data = request.data, partial=True)
    if serializer.is_valid():
        if 'image' in request.data:
            image = serializer.validated_data['image']
            if image:
                upload_result = cloudinary.uploader.upload(
                image,
                folder='posts'
                )
            image_url = upload_result['secure_url']
            serializer.validated_data['image'] = image_url
        serializer.save()
        return Response("Post is edited successfully",status=status.HTTP_200_OK)
    else:
        print(serializer.errors,'errrororrr')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(responses=postSerializer)
@api_view(['DELETE'])
def delete_post(request,id):
    post=Post.objects.get(id=id)
    post.delete()
    return Response("Post deleted")
    


@extend_schema(responses=eventSerializer)
@api_view(['POST'])
def add_event(request):
    serializer = eventSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'status': 'Event created successfully'},status=status.HTTP_201_CREATED) 
    print(serializer.errors,'errrorrs.....')
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

@extend_schema(responses=postSerializer)
@api_view(['GET'])
def event_list(request):
    events = Event.objects.all()
    serialized_events = []
    
    for event in events:
        event_data = eventSerializer(event).data
        event_data['artist_name'] = event.conducting_artist.artistname  # Fetch the artist's username
          # Add the artist's username to the serialized post data
        event_data['artist_id'] = event.conducting_artist.id  # Fetch the artist's id
        profile_image = event.conducting_artist.profile_img  # Fetch the artist's profileimg
        if profile_image:
            event_data['artist_profileimg'] = profile_image.url
        else:
            event_data['artist_profileimg'] = None
        serialized_events.append(event_data)
    # serializer = eventSerializer(events,many=True)
    return Response(serialized_events,status=status.HTTP_200_OK)


@api_view(['PATCH'])
def edit_event(request,id):
    event = Event.objects.get(id=id)
    serializer = eventSerializer(event,data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response("Post is edited successfully")
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(responses=postSerializer)
@api_view(['DELETE'])
def delete_event(request,id):
    event=Event.objects.get(id=id)
    event.delete()
    response = {'success': 'Event deleted successfully'}
    return Response(response,status=status.HTTP_200_OK)


@extend_schema(responses=bookingSerializer)
@api_view(['PATCH'])
def book_event(request):
    booking_serializer = bookingSerializer(data=request.data, partial=True)
    if booking_serializer.is_valid():
        booking_serializer.save()
        return Response({'status': 'Event booked successfully'}, status=status.HTTP_201_CREATED)
    print(booking_serializer.errors,'boooooking errroooorrrsss')
    return Response(booking_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def bookedevent_userlist(request,artist_id):
    booked_list = Booking.objects.filter(artist_id=id)
    serializer = bookingSerializer(booked_list,many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)


@extend_schema(responses=addressSerializer)
@api_view(['POST'])
def add_artistaddress(request):
    serializer = addressSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response("New address added succesfully", status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(responses=addressSerializer)
@api_view(['GET'])
def get_address(request,artistid):
    adresses = Address.objects.filter(artist_id=artistid)
    serializer = addressSerializer(adresses,many=True)
    return Response({'data':serializer.data},status=status.HTTP_200_OK)


@extend_schema(responses=bookingSerializer)
@api_view(['PATCH'])
def order_post(request):
    order_serializer = orderSerializer(data=request.data, partial=True)
    if order_serializer.is_valid():
        order_serializer.save()
        return Response({'status': 'Event booked successfully'}, status=status.HTTP_201_CREATED)
    print(order_serializer.errors,'boooooking errroooorrrsss')
    return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(responses=addressSerializer)
@api_view(['GET'])
def get_orders(request,artist_id):
    orders = Order.objects.filter(art_seller=artist_id)
    serializer = orderSerializer(orders,many=True)
    return Response({'data':serializer.data},status=status.HTTP_200_OK)


@api_view(['PATCH'])
def editorder_status(request):
    order_id = request.GET.get('order_id')
    value = request.GET.get('value')
    try:
        order = Order.objects.get(id=order_id)
        order.status = value
        order.order_status.save()
        serializer = orderSerializer(order)
        return Response(serializer.data,status=status.HTTP_200_OK)
    except:
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
def order_cancel(request,order_id):
    try:
        order = Order.objects.get(id='order_id')
        if order.order_status != 'Cancelled' :
            order.order_status = 'Cancelled'
            order.save()
            serializer = orderSerializer(order,many=False)
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response('Order is already cancelled',status=status.HTTP_400_BAD_REQUEST)
    except Order.DoesNotExist:
        return Response('Order not found',status=status.HTTP_404_NOT_FOUND)
    

@api_view(['GET'])
def order_details(request):
    orders = Order.objects.all()
    serializer = orderSerializer(orders,many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)