

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
#--------------------------------------------------------#
from rest_framework_simplejwt.tokens import RefreshToken
#--------------------------------------------------------#

# class CustomUserManager(BaseUserManager):
#     def create_user(self, email, username, password=None, **extra_fields):
#         if not email:
#             raise ValueError('The Email field must be set')
#         email = self.normalize_email(email)
#         user = self.model(email=email, username=username, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, username, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         return self.create_user(email, username, password, **extra_fields)
    
class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, full_name=None, phone_number=None, date_of_birth=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, full_name=full_name, phone_number=phone_number, date_of_birth=date_of_birth, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, full_name=None, phone_number=None, date_of_birth=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, username, password, full_name, phone_number, date_of_birth, **extra_fields)


#------------------------------------------------------------------------#

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    phone_number =models.DecimalField(blank=True,null=True,max_digits=10,decimal_places=0)
    date_of_birth = models.DateField(null=True)
    username = models.CharField(max_length=30)
    full_name=models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    account_created = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','full_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh':str(refresh),
            'access':str(refresh.access_token)
        }
    