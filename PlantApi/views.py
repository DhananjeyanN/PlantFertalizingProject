from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
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
        print('UPDATE DATATABLE')
        data_entry = get_object_or_404(DataTable, uuid=entry_id)
        plant_id = request.data['plant_id']
        plant_obj = get_object_or_404(Plant, id=plant_id)
        data = request.data
        data['plant'] = plant_obj.id
        data.pop('plant_id')
        print(data_entry, 'beannnnnns')
        print(data_entry.__dict__)
        print(data, 'THE DATA')
        if data['m_temp'] != 'None':
            data['m_temp'] = float(data.get('m_temp', None))
        else:
            data['m_temp'] = None
        if data['m_moist'] != 'None':
            data['m_moist'] = float(data.get('m_moist', None))
        else:
            data['m_moist'] = None
        if data['m_ec'] != 'None':
            data['m_ec'] = float(data.get('m_m_ec', None))
        else:
            data['m_ec'] = None
        if data['m_nitrogen'] != 'None':
            data['m_nitrogen'] = float(data.get('m_nitrogen', None))
        else:
            data['m_nitrogen'] = None
        if data['m_phosphorus'] != 'None':
            data['m_phosphorus'] = float(data.get('m_phosphorus', None))
        else:
            data['m_phosphorus'] = None
        if data['m_potassium'] != 'None':
            data['m_potassium'] = float(data.get('m_potassium', None))
        else:
            data['m_potassium'] = None
        if data['m_ph'] != 'None':
            data['m_ph'] = float(data.get('m_ph', None))
        else:
            data['m_ph'] = None
        data['date_time'] = datetime.strptime(data['date_time'], '%Y-%m-%d %H:%M:%S')
        print(data, 'daaaaaata')

        # {'plant_id': 2, 'uuid': 'cc09a0a8-c161-4115-8640-fe8e68e5e73a', 'm_temp': 1.0, 'm_moist': 2.0, 'm_ec': 1.0, 'm_npk': 2.0, 'm_ph': 1.0, 'date_time': datetime.datetime(2023, 10, 3, 4, 2, 15, 197382, tzinfo=datetime.timezone.utc)}
        # {'plant_id': 2, 'uuid': 'cc09a0a8-c161-4115-8640-fe8e68e5e73a', 'm_temp': '999.000000', 'm_moist': '888.000000', 'm_ec': '333.000000', 'm_npk': '123.000000', 'm_ph': '11.000000', 'date_time': '2023-09-30 20:49:03'}


        if request.method == 'POST' or request.method == 'PUT':
            serializer = DataTableSerializer(data_entry, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=200)
            else:
                print(serializer.errors, 'ERRRROR')
                return Response(serializer.errors, status=400)
    except Exception as error:
        print(error, 'THIS IS AN ERROR')
        return Response({'Error': 'Data entry not found In Update Plant!!!'}, status=404)


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
    print(request.data, 'HELLOB')
    if request.method == 'POST':
        plant_id = request.data['plant_id']
        plant_obj = get_object_or_404(Plant, id = plant_id)
        data = request.data
        print(request.data, 'ADDING', plant_obj.id)
        data['plant'] = plant_obj.id
        data.pop('plant_id')
        print(request.data, 'ADDING', plant_obj.id)
        print(type(data['m_temp']), 'MTEMPGG')
        if data['m_temp'] != 'None':
            data['m_temp'] = float(data.get('m_temp',None))
        else:
            data['m_temp'] = None
        if data['m_moist'] != 'None':
            data['m_moist'] = float(data.get('m_moist',None))
        else:
            data['m_moist'] = None
        if data['m_ec'] != 'None':
            data['m_ec'] = float(data.get('m_m_ec',None))
        else:
            data['m_ec'] = None
        if data['m_nitrogen'] != 'None':
            data['m_nitrogen'] = float(data.get('m_nitrogen',None))
        else:
            data['m_nitrogen'] = None
        if data['m_phosphorus'] != 'None':
            data['m_phosphorus'] = float(data.get('m_phosphorus',None))
        else:
            data['m_phosphorus'] = None
        if data['m_potassium'] != 'None':
            data['m_potassium'] = float(data.get('m_potassium',None))
        else:
            data['m_potassium'] = None
        if data['m_ph'] != 'None':
            data['m_ph'] = float(data.get('m_ph',None))
        else:
            data['m_ph'] = None
        data['date_time'] = datetime.strptime(data['date_time'], '%Y-%m-%d %H:%M:%S')

        serializer = DataTableSerializer(data=data)
        if serializer.is_valid():
            print(serializer)
            serializer.save()
            return Response(serializer.data, status=201) #201 means created succefully
        else:
            print(serializer.errors)
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


