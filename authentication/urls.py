from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

#------------------------------------------------------------------------#

urlpatterns = [
    path('register/',RegisterView.as_view(), name = "register" ), #registration url
    path('login/',LoginAPIView.as_view(), name = "login" ), #login url
    path('demo-recaptcha/', demo_recaptcha, name="demo"),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), #refresh token url 
    #  #RESET PASSWORD EMAIL REQUEST - VERIFY - RESET PASSWORD
    path('request-reset-email/', RequestPasswordResetEmail.as_view(), name='request-reset-email'), 
    path('password-reset/<uidb64>/<token>/', PasswordTokenCheckAPIView.as_view(), name = 'password-reset-confirm'),
    path('password-reset/',SetNewPasswordAPIView.as_view(), name = 'reset-password'),
    path('change-password/',ChangePasswordAfterLoginView.as_view(), name = 'change-password'),
]
