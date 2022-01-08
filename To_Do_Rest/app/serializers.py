from .models import *
from rest_framework import serializers
from rest_framework import exceptions
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, get_user_model
import django.contrib.auth.password_validation as validators
from rest_framework.authtoken.models import Token
class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name')
        write_only_fields = ('password',)
        read_only_fields = ('id',)



# class LoginSerializers(serializers.Serializer):
#     username = serializers.CharField(max_length=255)
#     password = serializers.CharField()

#     def validate(self, data):
#         username = data.get('username','')
#         password = data.get('password','')
#         if username and password:
#             user = authenticate(username=username,password=password)
#             print(user)
#             if not user:
#                 msg = ('Unable to log in with provided credentials.')
#                 raise serializers.ValidationError(msg, code='authorization')
#         else:
#             msg = ('Must include "username" and "password".')
#             raise serializers.ValidationError(msg, code='authorization')
#         data['user'] = user
#         return data

class LoginSerializers(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField()

class TokenSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()
    class Meta:
        model = get_user_model()
        fields = ('token',)

    def get_token(self, obj):
        token = Token.objects.get(user=obj)
        if token is not None:
            return token.key
        else:
            return ''    

class TaskDataSerializers(serializers.ModelSerializer):
    class Meta:
        model = TaskData
        exclude =['user']

class PasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_current_password(self, value):
        # if not self.context['request'].user.check_password(value):
        #     raise serializers.ValidationError('Current password does not match')
        return value

    def validate_new_password(self, value):
        validators.validate_password(value)
        return value
