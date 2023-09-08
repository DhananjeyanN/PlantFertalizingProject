from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import PlantSerializer, DataTableSerializer
from Core.models import Plant, DataTable
from Core.models import Plant
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class PlantListCreateView(generics.ListCreateAPIView):
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]


class DataTableListCreateView(generics.ListCreateAPIView):
    queryset = DataTable.objects.all()
    serializer_class = DataTableSerializer
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]


@csrf_exempt
@api_view(['POST', 'PUT'])
def update_plant(request, plant_id):
    try:
        plant = Plant.object.get(pk=plant_id)
        print(plant)
    except Plant.DoesNotExist:
        return Response({'Error': 'Plant Not Found!!!'}, status=404)
    if request.method == 'GET':
        serializer = PlantSerializer(plant)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = PlantSerializer(plant, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
