from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response

from .serializers import PlantSerializer, DataTableSerializer
from Core.models import Plant, DataTable
from Core.models import Plant
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication



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


# @csrf_exempt
@api_view(['POST', 'PUT'])
def update_plant(request, plant_id):
    if request.method == 'GET':
        return Response({'message': 'GET request received'}, status=200)
    try:
        plant = Plant.objects.get(pk=plant_id)
        print(plant)
    except Plant.DoesNotExist:
        return Response({'Error': 'Plant Not Found!!!'}, status=404)
    if request.method == 'POST' or request.method == 'PUT':
        serializer = PlantSerializer(plant, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)


@csrf_exempt
@api_view(['POST', 'PUT'])
def update_data_table_entry(request, entry_id):
    if request.method == 'GET':
        return Response({'message': 'GET request received'}, status=200)

    try:
        data_entry = DataTable.objects.get(pk=entry_id)
        print(data_entry)
    except DataTable.DoesNotExist:
        return Response({'Error': 'Data entry not found!'}, status=404)

    if request.method == 'POST' or request.method == 'PUT':
        serializer = DataTableSerializer(data_entry, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)
