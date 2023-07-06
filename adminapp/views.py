import json
import jwt
import base64
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics,permissions
from rest_framework.permissions import BasePermission, IsAuthenticated
from drf_spectacular.utils import extend_schema
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.hashers import check_password
from accounts.models import Accounts
from artist.models import Artist,Event, Post
from artist.serializers import artistSerializer, eventSerializer, postSerializer
from userapp.models import Order
from userapp.serializers import orderSerializer, userSerializer
# Create your views here.


class adminLogin(APIView):
    def post(self,request):
        email=request.data['email']
        password=request.data['password']
        try:
            admin = Accounts.objects.get(email=email)
            if admin.is_superuser:
                if admin.email==email:
                    if check_password(password,admin.password):
                        payload = {
                            'email' : email,
                            'password' : password
                        }
                        jwt_token = jwt.encode({'payload':payload},'secret',algorithm='HS256')
                        response = Response(
                        {'status': 'Success','payload':payload,'jwt':jwt_token,'role':'admin'})
                        return response
                    else:
                        status = 'Wrong Password'
                else:
                    status = 'Wrong Username'
            return Response({'status':status})
        except:
            if Accounts.DoesNotExist:
                return Response("Email or Password is Wrong")


# class adminLogin(APIView):
#     @extend_schema(responses=userSerializer,request=userSerializer)
#     def post(self,request):
#         serializer = userSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         email = serializer.validated_data['email']
#         password = serializer.validated_data['password']

#         try:
#             admin = Accounts.objects.get(email=email)
#             if admin.is_superuser and admin.email == email and check_password(password,admin.password):
#                 payload = {
#                     'email' : email,
#                     'password' : password
#                 }
#                 jwt_token = jwt.encode({'payload' : payload}, 'secret' , algorithm='HS256')
#                 response = {
#                     'status' : 'Success',
#                     'payload' : payload,
#                     'jwt' : jwt_token,
#                     'role' : 'admin'
#                 }
#                 return Response(response)
#             else:
#                 return Response({'status' : 'Invalid credentials'})
#         except:
#             if Accounts.DoesNotExist:
#                 return Response({'status' : "Email or Password is Wrong"})



@api_view(["GET"])
def Admin_Logout(request):
	response = Response(status=status.HTTP_200_OK)
	response.clear('jwt')
	return response



class IsAthenticatedOrReadOnly(BasePermission):
    """The request is authenticated as a user, or is a read-only request."""
    def has_permission(self, request, view):
        return request.method in ['GET','HEAD','OPTIONS'] or request.user.is_authenticated



class UserList(generics.ListAPIView):
    serializer_class = userSerializer
    permission_classes = [IsAthenticatedOrReadOnly]
    
    @extend_schema(responses=userSerializer)
    def get_queryset(self):
        response = Accounts.objects.all().exclude(is_superuser=True)
        return response


class UserView(APIView):
    def get(self,request,user_id):
        user = get_object_or_404(Accounts,pk=user_id)
        return Response({'is_blocked': user.is_blocked})


@extend_schema(responses=userSerializer)
@api_view(['GET'])
def admin_profile(request,id):
    admin = Accounts.objects.get(id=id)
    serializer = userSerializer(admin,many=False)
    return Response(serializer.data)


@extend_schema(responses=userSerializer)
@api_view(['POST'])
def add_profile_image(request,id):
    admin = Accounts.objects.get(id=id)
    admin.image = request.data['image']
    admin.save()
    serializer = userSerializer(admin,many=False)
    return Response(serializer.data)


@extend_schema(responses=artistSerializer)
@api_view(['GET'])
def artist_list(request):
    artists = Artist.objects.all()
    serializer = artistSerializer(artists,many=True)
    return Response(serializer.data)


class ArtistView(APIView):
    def get(self,request,id):
        artist = get_object_or_404(Artist,pk=id)
        return Response({'is_blocked': artist.is_blocked})


class BlockUnblockArtistView(APIView):
    def patch(self,request,artist_id):
        artist =get_object_or_404(Artist,pk=artist_id)
        artist.is_blocked = not artist.is_blocked
        artist.save()
        return Response(status=status.HTTP_200_OK)
    

@extend_schema(responses=eventSerializer)
@api_view(['GET'])
def event_list(request):
    events = Event.objects.all()
    serializer = eventSerializer(events,many=True)
    return Response(serializer.data)


@api_view(['DELETE'])
def delete_event(request,id):
    event = Event.objects.get(id=id)
    event.delete()
    return Response("Event deleted")


@extend_schema(responses=eventSerializer)
@api_view(['GET'])
def post_list(request):
    posts = Post.objects.all()
    serializer = postSerializer(posts,many=True)
    return Response(serializer.data)


@api_view(['DELETE'])
def delete_post(request,id):
    post = Post.objects.get(id=id)
    post.delete()
    return Response("Post deleted Successfully")


@api_view(['GET'])
def order_list(request):
    orders = Order.objects.all()
    serializer = orderSerializer(orders,many=True)
    return Response(serializer.data)


@api_view(['PATCH'])
def block_user(request,user_id):
    user = Accounts.objects.get(id=user_id)
    if user.is_blocked:
        print("user is blocked")
        user.is_blocked = False
        user.save()
    else:
        print("user is not blocked")
        user.is_blocked = True
        user.save()
    return Response({'status':'true'})


@api_view(['PATCH'])
def block_artist(request,artist_id):
    artist = Artist.objects.get(id=artist_id)
    if  artist.is_blocked:
        print("artist is blocked")
        artist.is_blocked = False
        artist.save()
    else:
        print("artist is not blocked")
        artist.is_blocked = True
        artist.save()
    return Response({'status':'true'})