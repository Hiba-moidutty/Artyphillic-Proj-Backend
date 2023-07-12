import jwt
import cloudinary.uploader 
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from drf_spectacular.utils import extend_schema
from django.shortcuts import get_object_or_404, render
from accounts.models import Accounts, Address
from artist.models import Artist, Event, Post
from artist.serializers import eventSerializer, postSerializer
from userapp.models import Booking, Order 
from .serializers import addressSerializer, bookingSerializer, orderSerializer, paymentSerializer, userSerializer
# Create your views here.


@extend_schema(responses=userSerializer)
@api_view(['POST'])
def verify_token(request):
    print(request.headers,'kkkkkkkkkkkkkk')
    token = request.data['token']
    decoded = jwt.decode(token,'secret',alogrithms='HS256')
    admi_n = Accounts.objects.get(email = decoded.get('email'))
    serializer = userSerializer(admi_n,many=False)
    if admi_n:
        return Response(serializer.data)
    else:
        return Response({'status': 'Token Invalid'})  


@extend_schema(responses=userSerializer(many=False))
@api_view(['GET'])
def user_profile(request,id):
    try:
        user = Accounts.objects.get(id=id)
        serializer = userSerializer(user,many=False)
        user_details = serializer.data
        return Response({'data':user_details}, status=status.HTTP_200_OK)
    except Accounts.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def userProfilePic(request, user_id):
    user = Accounts.objects.get(id=user_id)   # Assuming the artist is authenticated
    profile_picture = request.FILES["profile_img"]
    if profile_picture:
        upload_result = cloudinary.uploader.upload(
            profile_picture,
            folder='profiles'
        )
        print(upload_result, 'lllllllllllllll')
        profile_picture_url = upload_result['secure_url']
       # Update the profile_img field with the image URL
        user.profile_img = profile_picture_url
        user.save()
        return Response({"profile_picture_url": profile_picture_url})
    else:
        return Response({"message": "Unsuccessful"})


@api_view(['POST'])
def userCoverPic(request, user_id):
    user = Accounts.objects.get(id=user_id)   # Assuming the artist is authenticated
    cover_picture = request.FILES["cover_img"]
    if cover_picture:
        upload_result = cloudinary.uploader.upload(
            cover_picture,
            folder='profiles'
        )
        print(upload_result, 'lllllllllllllll')
        cover_picture_url = upload_result['secure_url']
       # Update the cover_img field with the image URL
        user.cover_img = cover_picture_url
        user.save()
        return Response({"profile_picture_url": cover_picture_url})
    else:
        return Response({"message": "Unsuccessful"})
    


@extend_schema(responses=userSerializer)
@api_view(['PUT'])
def user_profile_update(request,id):
    try:
        user = Accounts.objects.get(id=id)
        serializer = userSerializer(user,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("Profile updated Successfully")
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Accounts.DoesNotExist:
        return Response("Artist bot found", status=status.HTTP_404_NOT_FOUND )


@extend_schema(responses=eventSerializer)
@api_view(['GET'])
def event_details(request,id):
    events = Event.objects.filter(conducting_artist_id=id)
    serializer = eventSerializer(events,many=True)
    return Response(serializer.data)


@extend_schema(responses=bookingSerializer)
@api_view(['PATCH'])
def booking_event(request):
    booking_serializer = bookingSerializer(data=request.data)
    if booking_serializer.is_valid() :
        booking_data = booking_serializer.validated_data
        event_id = booking_data['eventname'].id
        slot_no = booking_data['slot_no']
        # Get the event
        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return Response({'error': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)
        # Check if the total_slots is already zero
        if event.total_slots == 0:
            return Response({'error': 'No available slots'}, status=status.HTTP_400_BAD_REQUEST)
        # Calculate the new total_slots value
        new_total_slots = event.total_slots - slot_no
        if new_total_slots < 0:
            new_total_slots = 0
        # Update the event's total_slots
        event.total_slots = new_total_slots
        event.save()
        # Save the booking
        booking_serializer.save()
        return Response({'status': 'Event booked successfully'}, status=status.HTTP_201_CREATED)
    return Response(booking_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(responses=bookingSerializer)
@api_view(['GET'])
def bookedevent_list(request,id):
    booked_list = Booking.objects.filter(username=id)
    serializer = bookingSerializer(booked_list,many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)
    



@extend_schema(responses=postSerializer)
@api_view(['GET'])
def artists_postlist(request,artist_id):
    posts = Post.objects.filter(artist_id = artist_id)
    serializer = postSerializer(posts,many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)


# @extend_schema(responses=postSerializer)
# @api_view(['GET'])
# def buy_post(request,post_id):
#     try:
#         address = Address.objects.get(user=request.user)
#         post = Post.objects.get(id=post_id)
#         base_price = post.base_price
#         shipping_price = post.shipping_price
#         total_price = base_price + shipping_price
#         data = {
#             'post':post.id,'base_price':base_price,
#             'shipping_price':shipping_price,'total_price':total_price,
#             'address':address
#             } 
#         return Response(data, status=status.HTTP_201_CREATED)
#     except Post.DoesNotExist:
#         return Response({'status':'Post not found'},status=status.HTTP_400_BAD_REQUEST)
    

@extend_schema(responses=addressSerializer)
@api_view(['POST'])
def add_address(request):
    serializer = addressSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response("New address added succesfully", status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(responses=addressSerializer)
@api_view(['GET'])
def address_details(request,userid):
    adresses = Address.objects.filter(user_id=userid)
    serializer = addressSerializer(adresses,many=True)
    return Response({'data':serializer.data},status=status.HTTP_200_OK)


@extend_schema(responses=addressSerializer)
@api_view(['DELETE'])
def delete_address(request,id):
    address = get_object_or_404(Address,id=id)
    address.delete()
    return Response("Address deleted successfully")


@extend_schema(responses=orderSerializer)
@api_view(['POST'])
def checkout(request):
    serializer = orderSerializer(data=request.data)
    if serializer.is_valid():
        order = serializer.save()
        return Response('Order placed successfully',status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@extend_schema(responses=orderSerializer)
@api_view(['GET'])
def order_list(request,order_id):
    order_list = Order.objects.filter(id=order_id)
    serializer = orderSerializer(order_list,many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)
    

@api_view(['PATCH'])
def ordercancel(request,id):
    order = Order.objects.get(id=id)
    if order.status != 'Cancelled':
        order.order_status = 'Cancelled'
        order.save()
        serializer = orderSerializer(order,many=False)
        return Response(serializer.data,status.HTTP_200_OK)
    else:
        return Response('Order is already cancelled',status=status.HTTP_400_BAD_REQUEST)
     