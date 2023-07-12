import json
import jwt
import base64
import cloudinary.uploader 
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from django.contrib.auth.hashers import make_password,check_password
from django.shortcuts import render
from accounts.models import Accounts
from artist.authentication import create_jwt_token_user
from userapp.serializers import userSerializer



@extend_schema(responses=userSerializer)
@api_view(['POST'])
def userSignUp(request):
    first_name = request.data['first_name']
    last_name = request.data['last_name']
    username = request.data['username']
    email = request.data['email']
    phone_number = request.data['phone_number']
    password = make_password(request.data['password'])

    if len(first_name) < 4:
        return Response({'status': 'Name should be a minimum of 4 letters'})
    if len(password) < 6:
        return Response({'status': 'Password should be a minimum of 6 characters'})

    check_user = Accounts.objects.all()
    for i in check_user:
        if i.email == email:
            return Response({'status': 'Email already exists'})
        elif i.phone_number == phone_number:
            return Response({'status': 'Phone Number already exists'})

    profile_image = "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png"
    upload_result = cloudinary.uploader.upload(
        profile_image,
        folder='profiles'
    )
    cover_image = "https://cdn.pixabay.com/photo/2017/12/28/15/06/geometric-3045402_1280.png"
    upload_result = cloudinary.uploader.upload(
        cover_image,
        folder='profiles'
    )
    cover_picture = upload_result['secure_url']
    print("success")
    user = Accounts.objects.create(
        first_name=first_name, last_name=last_name,
        username=username, email=email, phone_number=phone_number,
        password=password, cover_img=cover_image, profile_img=profile_image
    )
    user.save()
    serializer = userSerializer(user, many=False)
    return Response(serializer.data)


@extend_schema(responses=userSerializer)
@api_view(['POST'])
def userLogin(request):
    email = request.data['email']
    password = request.data['password']
    if not email or not password:
        return Response({'status': 'Please provide details (email, password)'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        user = Accounts.objects.get(email=email)
    except Accounts.DoesNotExist:
        return Response({'status':'Email or Password is incorrect'}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        print(e)
        return Response({'status': 'An error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    if check_password(password, user.password):
        jwt_token = create_jwt_token_user(user.id)
        data = {
            'id': user.id,
            'name':user.username,
            'email': user.email,
            'password': user.password,
            'token': jwt_token,
            'role': 'user'
        }
        return Response(data=data, status=status.HTTP_200_OK)
    else:
        return Response({'status': 'Email or Password is incorrect'}, status=status.HTTP_401_UNAUTHORIZED)

		
		


# @api_view(["GET"])
# def Logout(request):
# 	response = Response(status=status.HTTP_200_OK)
# 	response.clear('jwt')
# 	return response