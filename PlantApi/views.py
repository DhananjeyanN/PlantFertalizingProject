from django.http import JsonResponse
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
@api_view(['GET'])
def get_plant(request, plant_id):
    try:
        plant = Plant.objects.get(pk=plant_id)
    except Plant.DoesNotExist:
        return Response({'Error': 'Plant Not Found!!!'}, status=404)

    serializer = PlantSerializer(plant)
    return Response(serializer.data)\

@api_view(['GET'])
def get_all_plants(request):
    try:
        plants = Plant.objects.filter(user=request.user)
        serializer = PlantSerializer(plants, many=True)
        return JsonResponse(serializer.data, safe=False)
    except Plant.DoesNotExist:
        return Response({'Error': 'Plant Not Found!!!'}, status=404)


@csrf_exempt
@api_view(['POST', 'PUT'])
def update_plant(request, plant_id):
    if request.method == 'GET':
        return Response({'message': 'GET request received'}, status=200)

    try:
        plant_entry = Plant.objects.get(pk=plant_id)
    except Plant.DoesNotExist:
        return Response({'Error': 'plant not found!'}, status=404)

    if request.method == 'POST' or request.method == 'PUT':
        data = request.data
        data['user'] = request.user.id
        print(data)
        serializer = PlantSerializer(plant_entry, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        else:
            return Response(serializer.errors, status=400)\



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
            return Response(serializer.data, status=200)
        else:
            return Response(serializer.errors, status=400)\


@csrf_exempt
@api_view(['GET'])
def read_data_table_entry(request, entry_id):
    if request.method == 'GET':
        return Response({'message': 'GET request received'}, status=200)

    try:
        data_entry = DataTable.objects.get(pk=entry_id)
        return data_entry
    except DataTable.DoesNotExist:
        return Response({'Error': 'Data entry not found!'}, status=404)

@csrf_exempt
@api_view(['POST'])
def create_data_table_entry(request):
    if request.method == 'POST':
        serializer = DataTableSerializer(data=request.data)
        if serializer.is_valid():
            print(serializer)
            serializer.save()
            return Response(serializer.data, status=201) #201 means created succefully
        else:
            return Response(serializer.errors, status=400) # 400 means some error but found


@csrf_exempt
@api_view(['DELETE'])
def del_data_table_entry(request, entry_id):
    try:
        data_entry = DataTable.objects.get(pk=entry_id)
        print(data_entry)
    except DataTable.DoesNotExist:
        return Response({'Error': 'Data entry not found!'}, status=404)

    if request.method == 'DELETE':
        data_entry.delete()
        return Response({'message': 'Data Entry Deleted'}, status=204)


