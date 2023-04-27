from django.urls import path
from .views import *
urlpatterns = [
    
    # path('deleteuser/', DeleteGeoserverUser.as_view(),name = "createuser"),
    path('sugarlog/', BloodSugarLogListCreateAPIView.as_view(),name = "bloodsufarlog"),


]