from datetime import datetime, timedelta
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from Core.forms import AddPlantForm, EditPlantForm
from Core.models import Plant, DataTable
from accounts.models import SiteProfile
import json


# Create your views here.
def index(request):
    profile = SiteProfile.objects.all().first()
    plants = Plant.objects.all()
    plant_names = [plant.name for plant in plants]
    plant_temperatures = [plant.temperature for plant in plants]
    context = {'plants': plants, 'names': plant_names, 'temps': plant_temperatures, 'profile': profile}
    return render(request, 'Core/home.html', context=context)


def reg_index(request, plant_id=0):
    profile = SiteProfile.objects.all().first()
    if request.user.is_authenticated:

        plants = Plant.objects.filter(user=request.user)
        plant_names = [plant.name.replace(" ", "_") for plant in plants]
        data = {}
        detail_data = {}
        last_24_hours_ago = datetime.now() - timedelta(hours=1000)
        latest_data = []
        for plant in plants:
            plant_dict = {}
            plant_data = DataTable.objects.filter(plant=plant, date_time__gte=last_24_hours_ago)
            ec_exists = DataTable.objects.filter(plant=plant).exclude(m_ec__isnull=True).exists()
            if ec_exists:
                latest_ec_data = DataTable.objects.filter(plant=plant).exclude(m_ec__isnull=True).latest('date_time')
                plant_dict['latest_ec'] = latest_ec_data.m_ec
                plant_dict['latest_ph'] = latest_ec_data.m_ph
                plant_dict['latest_npk'] = latest_ec_data.m_npk
                plant_dict['latest_temp'] = latest_ec_data.m_temp
                plant_dict['latest_moist'] = latest_ec_data.m_moist
            else:
                plant_dict['latest_ec'] = None
                plant_dict['latest_ph'] = None
                plant_dict['latest_npk'] = None
                plant_dict['latest_temp'] = None
                plant_dict['latest_moist'] = None
            plant_dict['name'] = plant.name
            latest_data.append(plant_dict)

            data_key = plant.name.replace(" ", "_")
            data[data_key] = {}
            data[data_key]['date_time'] = [plant_data_item.date_time.isoformat() for plant_data_item in plant_data]
            data[data_key]['m_moist'] = [plant_data_item.m_moist for plant_data_item in plant_data]
            # For more detailed data
            detail_data[data_key] = {}
            detail_data[data_key]['date_time'] = [plant_data_item.date_time.isoformat() for plant_data_item in
                                                  plant_data]
            detail_data[data_key]['m_temp'] = [plant_data_item.m_temp for plant_data_item in plant_data]
            detail_data[data_key]['m_ec'] = [plant_data_item.m_ec for plant_data_item in plant_data]
            detail_data[data_key]['m_npk'] = [plant_data_item.m_npk for plant_data_item in plant_data]
            detail_data[data_key]['m_ph'] = [plant_data_item.m_ph for plant_data_item in plant_data]
        plant_ids = [plant.id for plant in plants]

        plant_temperatures = [plant.temperature for plant in plants]
        context = {'plants': plants, 'names': plant_names, 'temps': plant_temperatures, 'profile': profile,
                   'data': json.dumps(data), 'latest_data': latest_data, 'detail_data': json.dumps(detail_data),
                   "ids": json.dumps(plant_ids),
                   }
    else:
        context = {'profile': profile}
    return render(request, 'Core/reg_home.html', context=context)


# def add_plant(request):
#     if request.method == 'POST':
#         form = AddPlantForm(request.POST, request.FILES)  # Include request.FILES
#         if form.is_valid():
#             plant = form.save()
#             data = DataTable(plant=plant)
#             data.save()
#             messages.success(request, 'Plant Added Successfully!!!')
#             return redirect('index')
#         else:
#             messages.error(request, 'Invalid Form')
#     else:
#         form = AddPlantForm()
#     context = {
#         'form': form,
#     }
#     return render(request, 'add_plant.html', context)

def add_plant(request):
    if request.method == 'POST':
        name = request.POST.get('plant_name')
        pic = request.FILES.get('plant_pic')
        ec = request.POST.get('ec')
        ph = request.POST.get('ph')
        nitrogen = request.POST.get('nitrogen')
        potassium = request.POST.get('potassium')
        phosphorus = request.POST.get('phosphorus')
        temp = request.POST.get('temperature')
        ideal_moist = request.POST.get('ideal_moisture')
        fertilizer = request.POST.get('fertilizer')
        plant_coefficient = request.POST.get('plant_coefficient')
        plant = Plant(user=request.user, name=name, photo=pic, ec=ec, ph=ph, nitrogen=nitrogen, potassium=potassium, phosphorus=phosphorus, temperature=temp, ideal_moisture = ideal_moist, fertilizer=fertilizer, plant_coefficient=plant_coefficient)
        plant.save()
        return redirect('reg_index')


def update_plant(request, plant_id):
    print('UPDATING PLANT')
    if request.method == "POST":
        plant = Plant.objects.get(pk=plant_id)
        plant.ec = request.POST['ec']
        plant.ph = request.POST['ph']
        plant.npk = request.POST['npk']
        plant.temperature = request.POST['temperature']
        plant.ideal_moisture = request.POST['ideal_moisture']
        plant.fertilizer = request.POST['fertilizer']
        plant.save()
        print(plant.fertilizer, 'FERTILIZER')
        print(plant.ideal_moisture, request.POST, 'Ideal_temp')
        return redirect('reg_index')

    return JsonResponse({'status': 'error'})
