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
    second_password_question_1 = serializers.CharField(required=True)
    second_password_answer_1 = serializers.CharField(required=True)
    second_password_question_2 = serializers.CharField(required=True)
    second_password_answer_2 = serializers.CharField(required=True)
    second_password_question_3 = serializers.CharField(required=True)
    second_password_answer_3 = serializers.CharField(required=True)
    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password2', 'full_name', 'phone_number', 'date_of_birth',
                  'second_password_question_1', 'second_password_answer_1', 'second_password_question_2',
                  'second_password_answer_2', 'second_password_question_3', 'second_password_answer_3']
        extra_kwargs = {
            'password': {'write_only': True}
        }

class SendQAResponseSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField()
    tokens = serializers.DictField(child=serializers.CharField())
    security_questions = serializers.ListField(child=serializers.CharField(), required=False)

# class LoginSerializer(serializers.ModelSerializer):
#     email = serializers.EmailField(max_length=255, min_length = 3)
#     password = serializers.CharField(max_length=64, write_only=True)
#     username = serializers.CharField(max_length=255, min_length = 3, read_only=True)
#     tokens  = serializers.CharField(max_length=64, read_only=True)
    
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password','tokens']

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})

    # Add fields for the security questions and their answers
    second_password_question_1 = serializers.CharField(required=False)
    second_password_answer_1 = serializers.CharField(style={'input_type': 'password'}, write_only=True, required=False)
    second_password_question_2 = serializers.CharField(required=False)
    second_password_answer_2 = serializers.CharField(style={'input_type': 'password'}, write_only=True, required=False)
    second_password_question_3 = serializers.CharField(required=False)
    second_password_answer_3 = serializers.CharField(style={'input_type': 'password'}, write_only=True, required=False)

    def validate(self, data):
        # Check that all security questions have either been answered or not set
        if any([data.get(f'second_password_question_{i}') and not data.get(f'second_password_answer_{i}') for i in range(1, 4)]):
            raise serializers.ValidationError({'error': 'Security questions were provided without their answers.'})

        return data

class ResetPasswordEmailRequestSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(min_length=2)

    class Meta:
        model = User
        fields = ['email'] 

class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=6, max_length=64, write_only=True)
    password2 = serializers.CharField(min_length=6, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)
    
    class Meta:
        fields = ['password', 'password2','token','uidb64']

class ChangePasswordAfterLoginSerializer(serializers.Serializer):
    current_password = serializers.CharField(min_length=6, required=True, write_only=True)
    password = serializers.CharField(min_length=6, required=True, max_length=64, write_only=True)
    password2 = serializers.CharField(min_length=6, required=True, write_only=True)
    
    class Meta:
        model = User
        fields = ['current_password','password', 'password2']

    def validate_current_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Current password is incorrect')
        return value

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError('Passwords do not match')
    
        return data
