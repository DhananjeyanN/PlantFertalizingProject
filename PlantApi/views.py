from django.shortcuts import render
from rest_framework import generics
from .serializers import PlantSerializer
from Core.models import Plant
from Core.models import Plant
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class PlantListCreateView(generics.ListCreateAPIView):
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

