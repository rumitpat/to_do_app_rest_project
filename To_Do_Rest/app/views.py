from django.shortcuts import render
from .serializers import *
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import login,logout
import json
from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.parsers import JSONParser
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate

class SignupViewSet(APIView):
    def post(self,request):
        username=self.request.data.get('username')
        email=self.request.data.get('email')
        first_name=self.request.data.get('first_name')
        last_name=self.request.data.get('last_name')
        password =self.request.data.get('password')
        data ={
            "username":username,
            "email":email,
            "first_name":first_name,
            "last_name":last_name,
            "password":make_password(password)
        }
        serializer = SignupSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


def get_and_authenticate_user(username, password):
    user = authenticate(username=username, password=password)
    if user is None:
        raise serializers.ValidationError("Invalid username/password. Please try again!")
    # ensure to have a valid token
    Token.objects.get_or_create(user=user)
    return user

class LoginAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_and_authenticate_user(**serializer.validated_data)
        data = TokenSerializer(user).data
        data.update({'user':user.username})
        return Response(data=data, status=status.HTTP_200_OK)   

class LogoutAPIView(APIView):
    permission_classes =[IsAuthenticated]
    def get(self,request):
        request.user.auth_token.delete()
        logout(request)
        return Response({"status": status.HTTP_200_OK})


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def task_list_api(request):
    data =TaskData.objects.filter(user__username =request.user)
    serializeres= TaskDataSerializers(data,many=True)
    return Response(serializeres.data)


@permission_classes([IsAuthenticated])
@api_view(['POST'])
def task_create_api(request):
    serializer = TaskDataSerializers(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = TaskDataSerializers(serializer.validated_data).data
    TaskData.objects.create(user =request.user,**serializer.validated_data)
    return Response(data=data,status=status.HTTP_201_CREATED) 


@permission_classes([IsAuthenticated])
@api_view(['DELETE'])
def task_delete_api(request, pk):
    task_data_obj =TaskData.objects.filter(pk =pk).first()
    if task_data_obj is None:
        return Response({"status": "task not found."})
    if task_data_obj.user == request.user:
        task_data_obj.delete()
        return Response({"status": "Your Task Is Deleted."})
    else:
        return Response({"status": "You Do Not have Permession To delete Task."})    

        
@permission_classes([IsAuthenticated])
@api_view(['PUT'])
def task_update_api(request, pk):
    task_data_obj =TaskData.objects.filter(pk =pk).first()
    if task_data_obj is None:
        return Response({"status": "task not found."})
    if task_data_obj.user == request.user:
        serializer = TaskDataSerializers(task_data_obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response({"status": "You Do Not have Permession To update Task."})
    
    
@permission_classes([IsAuthenticated])
@api_view(['PATCH'])
def task_patch_api(request, pk):
    task_data_obj =TaskData.objects.filter(pk =pk).first()
    if task_data_obj is None:
        return Response({"status": "task not found."})
    if task_data_obj.user == request.user:
        serializer = TaskDataSerializers(datas, data=request.data,partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response({"status": "You Do Not have Permession To update Task."})    

    

@permission_classes([IsAuthenticated])
@api_view(['POST'])
def change_password_api(request):
    serializer = PasswordChangeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    request.user.set_password(serializer.validated_data['new_password'])
    request.user.save()
    return Response({"status": "Password Change Successfully.."})      