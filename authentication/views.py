from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from authentication.models import User
from django.core.exceptions import ValidationError
from .serializers import RegistrationSerializer,LoginSerializer
from rest_framework import generics
import re
from django.contrib import auth


from rest_framework.exceptions import ValidationError

class RegisterView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            if 'email' in e.detail and 'unique' in e.detail['email'][0].code.lower():
                return Response({'error': 'User with this email already exists.'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'error': e.detail}, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data

        username = validated_data['username']
        password = validated_data['password']
        email = validated_data['email'].lower()
        full_name = validated_data['full_name']
        phone_number = validated_data['phone_number']
        date_of_birth = validated_data['date_of_birth']

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({'error': 'User with this email already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        if username[0].isdigit():
            return Response({'error': 'Username cannot start with a number'}, status=status.HTTP_400_BAD_REQUEST)

        if " " in username:
            return Response({'error': 'Username cannot contain spaces'}, status=status.HTTP_400_BAD_REQUEST)

        if " " in password:
            return Response({'error': 'Password cannot contain spaces'}, status=status.HTTP_400_BAD_REQUEST)

        if len(username) < 3:
            return Response({'error': 'Username must be at least 3 characters'}, status=status.HTTP_400_BAD_REQUEST)

        if len(password) < 8:
            return Response({'error': 'Password should be at least 8 characters.'}, status=status.HTTP_400_BAD_REQUEST)
        if not re.search(r'[A-Z]', password):
            return Response({'error': 'Password should contain at least one uppercase letter.'}, status=status.HTTP_400_BAD_REQUEST)
        if not re.search(r'[a-z]', password):
            return Response({'error': 'Password should contain at least one lowercase letter.'}, status=status.HTTP_400_BAD_REQUEST)
        if not re.search(r'\d', password):
            return Response({'error': 'Password should contain at least one number.'}, status=status.HTTP_400_BAD_REQUEST)
        if not re.search(r'[.!@#$%^&*()_+}{":?><,./;\'\[\]\\|=~-]', password):
            return Response({'error': 'Password should contain at least one special character.'}, status=status.HTTP_400_BAD_REQUEST)

        if password != validated_data['password2']:
            return Response({'error': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(email=email, username=username, password=password, full_name=full_name, phone_number=phone_number, date_of_birth=date_of_birth)

        return Response({'details':'Account Created Successfully.'}, status=status.HTTP_201_CREATED)

# Create your views here.
# class RegisterView(generics.GenericAPIView):
#     serializer_class = RegistrationSerializer

#     def post(self, request, *args, **kwargs):
#         try:
#             serializer = self.get_serializer(data=request.data)
#             serializer.is_valid(raise_exception=True)
#         except ValidationError as e:
#             if 'email' in e.detail and 'unique' in e.detail['email'][0].code.lower():
#                 return Response({'error': 'User with this email already exists.'}, status=status.HTTP_400_BAD_REQUEST)
#             return Response({'error': e.detail}, status=status.HTTP_400_BAD_REQUEST)

#         validated_data = serializer.validated_data

#         username = validated_data['username']
#         password = validated_data['password']
#         email = validated_data['email'].lower()

#         if User.objects.filter(username=username).exists():
#             return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

#         if User.objects.filter(email=email).exists():
#             return Response({'error': 'User with this email already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        
#         if username[0].isdigit():
#             return Response({'error': 'Username cannot start with a number'}, status=status.HTTP_400_BAD_REQUEST)
        
#         if " " in username:
#             return Response({'error': 'Username cannot contain spaces'}, status=status.HTTP_400_BAD_REQUEST)
        
#         if " " in password:
#             return Response({'error': 'Password cannot contain spaces'}, status=status.HTTP_400_BAD_REQUEST)
            
#         if len(username) < 3:
#             return Response({'error': 'Username must be at least 3 characters'}, status=status.HTTP_400_BAD_REQUEST)
            
#         if len(password) < 8:
#             return Response({'error': 'Password should be at least 8 characters.'}, status=status.HTTP_400_BAD_REQUEST)
#         if not re.search(r'[A-Z]', password):
#             return Response({'error': 'Password should contain at least one uppercase letter.'}, status=status.HTTP_400_BAD_REQUEST)
#         if not re.search(r'[a-z]', password):
#             return Response({'error': 'Password should contain at least one lowercase letter.'}, status=status.HTTP_400_BAD_REQUEST)
#         if not re.search(r'\d', password):
#             return Response({'error': 'Password should contain at least one number.'}, status=status.HTTP_400_BAD_REQUEST)
#         if not re.search(r'[.!@#$%^&*()_+}{":?><,./;\'\[\]\\|=~-]', password):
#             return Response({'error': 'Password should contain at least one special character.'}, status=status.HTTP_400_BAD_REQUEST)
            
#         if password != validated_data['password2']:
#             return Response({'error': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)

#         user = User.objects.create_user(email=email, username=username, password=password)
        
        
#         return Response({'details':'Account Created Successfully.'}, status=status.HTTP_201_CREATED)
    
class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            validated_data = serializer.validated_data
            email = validated_data['email'].lower()
            password = validated_data['password']
        except ValidationError as e:
            return Response({'error': e.detail}, status=status.HTTP_400_BAD_REQUEST)
        
        user = auth.authenticate(email=email, password=password)


        if not user:
            return Response({'error': 'Email or Password is Incorrect, Please Try Again.'}, status=status.HTTP_400_BAD_REQUEST)
    
        if not user.is_active:
            return Response({'error': 'Account is Disabled, Contact Admin!'}, status=status.HTTP_400_BAD_REQUEST)
                
        # refresh = RefreshToken.for_user(user)
        # return Response({'username':str(user.username), 'email':str(user.email),'tokens': {'refresh': str(refresh), 'access': str(refresh.access_token)}}, status=status.HTTP_200_OK) 

        # Generate geoserver_token using the username field
        return Response({
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens(),
        })

    


       
