import jwt
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


@extend_schema(responses=userSerializer)
@api_view(['GET'])
def user_profile(request,id):
    artist = Accounts.objects.filter(id=id)
    serializer = userSerializer(artist,many=True)
    return Response(serializer.data)


@extend_schema(responses=userSerializer)
@api_view(['PUT'])
def user_profile_update(request,id):
    try:
        artist = Accounts.objects.get(id=id)
        serializer = userSerializer(artist,data=request.data)
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
@api_view(['POST'])
def booking_event(request):
    booking_serializer = bookingSerializer(data=request.data)
    if booking_serializer.is_valid() :
        booking_serializer.save()
        return Response({'status': 'Event booked successfully'}, status=status.HTTP_201_CREATED)
    return Response(booking_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(responses=bookingSerializer)
@api_view(['GET'])
def bookedevent_list(request,user_id):
    booked_list = Booking.objects.filter(user_id=id)
    serializer = bookingSerializer(booked_list,many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)
    



@extend_schema(responses=postSerializer)
@api_view(['GET'])
def artists_postlist(request,artist_id):
    posts = Post.objects.filter(artist_id = artist_id)
    serializer = postSerializer(posts,many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)


# @extend_schema(responses=postSerializer)
@api_view(['GET'])
def buy_post(request,post_id):
    try:
        address = Address.objects.get(user=request.user)
        post = Post.objects.get(id=post_id)
        base_price = post.base_price
        shipping_price = post.shipping_price
        total_price = base_price + shipping_price
        data = {
            'post':post.id,'base_price':base_price,
            'shipping_price':shipping_price,'total_price':total_price,
            'address':address
            } 
        return Response(data, status=status.HTTP_201_CREATED)
    except Post.DoesNotExist:
        return Response({'status':'Post not found'},status=status.HTTP_400_BAD_REQUEST)
    

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
def address_details(request):
    adresses = Address.objects.filter(user=request.user)
    serializer = addressSerializer(adresses,many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)


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
     