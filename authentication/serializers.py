from authentication.models import User
from rest_framework import serializers


# class RegistrationSerializer(serializers.ModelSerializer):
#     password2 = serializers.CharField(style = {'input_type':'password'}, write_only=True)
#     class Meta:
#         model = User
#         fields = ['full_name', 'email', 'phone_number','date_of_birth','username','password','password2','account_created']
#         extra_kwargs = {
#             'password': {'write_only': True}
#         }


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style = {'input_type':'password'}, write_only=True)
    class Meta:
        model = User
        fields = ['full_name', 'email', 'phone_number', 'date_of_birth', 'username', 'password', 'password2', 'account_created']
        extra_kwargs = {
            'password': {'write_only': True}
        }
class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length = 3)
    password = serializers.CharField(max_length=64, write_only=True)
    username = serializers.CharField(max_length=255, min_length = 3, read_only=True)
    tokens  = serializers.CharField(max_length=64, read_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password','tokens']