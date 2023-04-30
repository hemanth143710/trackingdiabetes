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


from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import Throttled
# from .serializers import UserCreateSerializer

from .throttle import UserLoginRateThrottle
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers

class RegisterView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer
    throttle_classes = (UserLoginRateThrottle,)

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            if 'email' in e.detail and 'unique' in e.detail['email'][0].code.lower():
                return Response({'error': 'User with this email already exists.'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'error': e.detail}, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data

         # check if the required fields are provided
        if not validated_data['second_password_question_1']:
            return Response({'error': 'Second password question 1 is required.'}, status=status.HTTP_400_BAD_REQUEST)

        if not validated_data['second_password_answer_1']:
            return Response({'error': 'Second password answer 1 is required.'}, status=status.HTTP_400_BAD_REQUEST)
        if not validated_data['second_password_question_2']:
            return Response({'error': 'Second password question 1 is required.'}, status=status.HTTP_400_BAD_REQUEST)

        if not validated_data['second_password_answer_2']:
            return Response({'error': 'Second password answer 1 is required.'}, status=status.HTTP_400_BAD_REQUEST)
        if not validated_data['second_password_question_3']:
            return Response({'error': 'Second password question 1 is required.'}, status=status.HTTP_400_BAD_REQUEST)

        if not validated_data['second_password_answer_3']:
            return Response({'error': 'Second password answer 1 is required.'}, status=status.HTTP_400_BAD_REQUEST)

        username = validated_data['username']
        password = validated_data['password']
        email = validated_data['email'].lower()
        full_name = validated_data['full_name']
        phone_number = validated_data['phone_number']
        date_of_birth = validated_data['date_of_birth']
        second_password_question_1 = validated_data.get('second_password_question_1')
        second_password_answer_1 = validated_data.get('second_password_answer_1')
        second_password_question_2 = validated_data.get('second_password_question_2')
        second_password_answer_2 = validated_data.get('second_password_answer_2')
        second_password_question_3 = validated_data.get('second_password_question_3')
        second_password_answer_3 = validated_data.get('second_password_answer_3')

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

        #user = User.objects.create_user(email=email, username=username, password=password, full_name=full_name, phone_number=phone_number, date_of_birth=date_of_birth)
        user = User.objects.create_user(email=email, username=username, password=password, full_name=full_name,
                                phone_number=phone_number, date_of_birth=date_of_birth,
                                second_password_question_1=second_password_question_1,
                                second_password_answer_1=second_password_answer_1,
                                second_password_question_2=second_password_question_2,
                                second_password_answer_2=second_password_answer_2,
                                second_password_question_3=second_password_question_3,
                                second_password_answer_3=second_password_answer_3)
        
        return Response({'details':'Account Created Successfully.'}, status=status.HTTP_201_CREATED)
    def throttled(self, request, wait):
        raise Throttled(detail={
            "error": "recaptcha_required",
        })
    
from django.shortcuts import render
from django.conf import settings

def demo_recaptcha(request):
    return render(request, 'demo_recaptcha.html', {
        "key": settings.RE_CAPTCHA_SITE_KEY
    })

# class RegisterUserAPIView(CreateAPIView):

#     permission_classes = [AllowAny]
#     serializer_class = UserCreateSerializer
#     throttle_classes = (UserLoginRateThrottle,)

#     def perform_create(self, serializer):
#         user = serializer.save()

#     def throttled(self, request, wait):
#         raise Throttled(detail={
#             "message": "recaptcha_required",
#         })

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
    
# class LoginAPIView(generics.GenericAPIView):
#     serializer_class = LoginSerializer
#     permission_classes = [AllowAny]
#     throttle_classes = (UserLoginRateThrottle,)

#     def post(self, request, *args, **kwargs):
        
#         try:
#             serializer = self.get_serializer(data=request.data)
#             serializer.is_valid(raise_exception=True)
#             validated_data = serializer.validated_data
#             email = validated_data['email'].lower()
#             password = validated_data['password']
#         except ValidationError as e:
#             return Response({'error': e.detail}, status=status.HTTP_400_BAD_REQUEST)
        
#         user = auth.authenticate(email=email, password=password)


#         if not user:
#             return Response({'error': 'Email or Password is Incorrect, Please Try Again.'}, status=status.HTTP_400_BAD_REQUEST)
    
#         if not user.is_active:
#             return Response({'error': 'Account is Disabled, Contact Admin!'}, status=status.HTTP_400_BAD_REQUEST)
                
#         # refresh = RefreshToken.for_user(user)
#         # return Response({'username':str(user.username), 'email':str(user.email),'tokens': {'refresh': str(refresh), 'access': str(refresh.access_token)}}, status=status.HTTP_200_OK) 

#         # Generate geoserver_token using the username field
#         return Response({
#             'email': user.email,
#             'username': user.username,
#             'tokens': user.tokens(),
#         })
#     def throttled(self, request, wait):
#         raise Throttled(detail={
#             "error": "recaptcha_required",
#         })

class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]
    throttle_classes = (UserLoginRateThrottle,)

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
        
        # Check if the user has set security questions
        if user.second_password_question_1 and user.second_password_question_2 and user.second_password_question_3:
            # If the user has set security questions, check their answers
            answers = {
                'question_1': user.second_password_answer_1,
                'question_2': user.second_password_answer_2,
                'question_3': user.second_password_answer_3
            }
            
            provided_answers = {
                'question_1': validated_data.get('second_password_answer_1', ''),
                'question_2': validated_data.get('second_password_answer_2', ''),
                'question_3': validated_data.get('second_password_answer_3', '')
            }
            
            if not all([provided_answers[k] == answers[k] for k in answers]):
                return Response({'error': 'Incorrect answer to one or more security questions.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Generate the tokens
        return Response({
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens(),
        },status=status.HTTP_200_OK)
        # refresh = RefreshToken.for_user(user)
        # return Response({
        #     'email': user.email,
        #     'username': user.username,
        #     'tokens': {'refresh': str(refresh), 'access': str(refresh.access_token)}
        # }, status=status.HTTP_200_OK) 

    def throttled(self, request, wait):
        raise Throttled(detail={
            "error": "recaptcha_required",
        })


from .serializers import SendQAResponseSerializer

class SendQAAPIView(generics.GenericAPIView):

    serializer_class = SendQAResponseSerializer
    permission_classes = [AllowAny]

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
        
        # check if security questions are already answered

        # if security questions not answered, return questions to frontend
        serializer = SendQAResponseSerializer({
            'email': user.email,
            'username': user.username,
            'security_questions': [
                user.second_password_question_1,
                user.second_password_question_2,
                user.second_password_question_3,
            ]
        })
        return Response(serializer.data)

    

from .serializers import ResetPasswordEmailRequestSerializer,SetNewPasswordSerializer,ChangePasswordAfterLoginSerializer
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import Util
from django.shortcuts import redirect
class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        try:
            serializer = self.serializer_class(data = request.data)

            email = request.data['email'].lower()
        except KeyError:
            return Response({'Error':'Email Field is Requried!'})

        if User.objects.filter(email=email).exists():
                user = User.objects.get(email = email)
                uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
                token = PasswordResetTokenGenerator().make_token(user)
                current_site = get_current_site(request = request).domain
                relative_link = reverse('password-reset-confirm', kwargs = {'uidb64':uidb64, 'token':token})
                absurl = "http://"+current_site+relative_link
                email_body = "Hello, " + user.username+","+"\nUse This Link Below To Reset Your Password \n"+ absurl
                data={'email_body':email_body,'to_email':user.email,'email_subject':'Reset your Password'}

                Util.send_email(data)

        else:
            return Response({'error':'The Email Id You have Entered is Incorrect!'})
        return Response({"success":"we have a sent you a link to reset your password!"}, status = status.HTTP_200_OK)

    
class PasswordTokenCheckAPIView(generics.GenericAPIView):
    def get(self, request, uidb64, token):
        try:
            id=smart_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error':'Token is not valid, Please Request a new one!'}, status=status.HTTP_401_UNAUTHORIZED)

            # return Response({"success": 'true', 'message':'credentials valid', 'uidb64':uidb64, 'token': token}, status = status.HTTP_200_OK)
            #return redirect('http://10.10.7.140/deduce_map/seotech-html/Forgotpass.html')
            return redirect(f'http://127.0.0.1:5500/td2/trackingdiabetes/templates/Forgotpass.html?uidb64={uidb64}&token={token}')
        except DjangoUnicodeDecodeError as Identifier:
            return Response({'error':'Link is not valid, Please Request a new one!'}, status=status.HTTP_401_UNAUTHORIZED  )
        
#SET NEW PASSWORD VIEW
class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)

            password = serializer.validated_data['password']
            password2 = serializer.validated_data['password2']
            token = serializer.validated_data['token']
            uidb64 = serializer.validated_data['uidb64']
        except ValidationError:
            return Response({'Error':'Password must be at least 7 characters'},status=status.HTTP_400_BAD_REQUEST)
        
        id = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=id)

        if not user:
            return Response({'Error':'Invalid Credentials, Please Try Again.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if len(password)<7:
            return Response({'Error':'Password must be at least 7 characters'}, status=status.HTTP_400_BAD_REQUEST)
        
        if password != password2:
            return Response({'Error':'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)
        
        if user.is_active == False:
            return Response({'Error':'Account is Disabled, Please Contact Our Team!'}, status=status.HTTP_400_BAD_REQUEST)
        

        if not PasswordResetTokenGenerator().check_token(user, token):
            return Response({'Error':'The Reset Token is Invalid!'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(password)
        user.save()

        return Response({'success':'true', 'Message':'Password Reset Successfull'})
    
class ChangePasswordAfterLoginView(generics.GenericAPIView):
    serializer_class = ChangePasswordAfterLoginSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError as e:
            error_dict = e.detail
            error_message = {}
            for field, errors in error_dict.items():
                error_message[field] = errors[0]
            return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)

        password = serializer.validated_data['password']
        password2 = serializer.validated_data['password2']
        if password != password2:
            return Response({'error': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)
        
        self.change_password(serializer.validated_data['password'])
        #return Response({'success': True, 'message': 'Password changed successfully'})
        return Response({'success':'true', 'Message':'Password Changed Successfully'}, status=status.HTTP_200_OK)
    

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return self.serializer_class
        return None

    def change_password(self, password):
        user = self.request.user
        user.set_password(password)
        user.save()


       
