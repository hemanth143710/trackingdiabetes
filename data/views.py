from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status
from rest_framework.response import Response
from .models import BloodSugarLog
from rest_framework.permissions import IsAuthenticated
from .serializers import BloodSugarLogSerializer

# class BloodSugarLogListCreateAPIView(generics.ListCreateAPIView):

#     serializer_class = BloodSugarLogSerializer
#     permission_classes = [IsAuthenticated]
#     def get_queryset(self):
#         return BloodSugarLog.objects.filter(user=self.request.user)

#     def post(self, request, *args, **kwargs):
#         serializer = BloodSugarLogSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(user=request.user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class BloodSugarLogListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = BloodSugarLogSerializer

    def get_queryset(self):
        return BloodSugarLog.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = BloodSugarLogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
