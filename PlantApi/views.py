from django.shortcuts import render
from rest_framework import generics
from .serializers import PlantSerializer
from Core.models import Plant
from Core.models import Plant


# Create your views here.
class PlantListCreateView(generics.ListCreateAPIView):
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer
