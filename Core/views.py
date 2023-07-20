from datetime import datetime, timedelta
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from Core.forms import AddPlantForm
from Core.models import Plant, DataTable
from accounts.models import SiteProfile
from django.http import JsonResponse
import json

# Create your views here.


def index(request):
    profile = SiteProfile.objects.all().first()
    plants = Plant.objects.all()
    plant_names = [plant.name for plant in plants]
    plant_temperatures = [plant.temperature for plant in plants]
    context = {'plants': plants, 'names': plant_names, 'temps': plant_temperatures, 'profile': profile}
    return render(request, 'Core/home.html', context=context)


def reg_index(request):
    profile = SiteProfile.objects.all().first()
    plants = Plant.objects.filter(user = request.user)
    plant_names = [plant.name.replace(" ", "_") for plant in plants]
    data = {}
    last_24_hours_ago = datetime.now() - timedelta(hours=500)
    latest_data = {}
    for plant in plants:
        plant_dict= {}
        plant_data = DataTable.objects.filter(plant=plant, date_time__gte = last_24_hours_ago)
        latest_ec_data = DataTable.objects.filter(plant= plant).exclude(m_ec__isnull =True).latest('date_time')
        plant_dict['latest_ec'] = latest_ec_data.m_ec
        latest_ph_data = DataTable.objects.filter(plant= plant).exclude(m_ph__isnull =True).latest('date_time')
        plant_dict['latest_ph'] = latest_ec_data.m_ph
        latest_npk_data = DataTable.objects.filter(plant= plant).exclude(m_npk__isnull =True).latest('date_time')
        plant_dict['latest_npk'] = latest_ec_data.m_npk
        latest_temp_data = DataTable.objects.filter(plant= plant).exclude(m_temp__isnull =True).latest('date_time')
        plant_dict['latest_temp'] = latest_ec_data.m_temp
        latest_moist_data = DataTable.objects.filter(plant= plant).exclude(m_moist__isnull =True).latest('date_time')
        plant_dict['latest_moist'] = latest_ec_data.m_moist
        latest_data[plant.name] = plant_dict
        data_key = plant.name.replace(" ", "_")
        data[data_key] = {}
        data[data_key]['date_time'] = [plant_data_item.date_time.isoformat() for plant_data_item in plant_data]
        data[data_key]['m_moist'] = [plant_data_item.m_moist for plant_data_item in plant_data]
    print(latest_data)
    plant_temperatures = [plant.temperature for plant in plants]
    context = {'plants': plants, 'names': plant_names, 'temps': plant_temperatures, 'profile': profile, 'data': json.dumps(data), 'latest_data': latest_data}
    return render(request, 'Core/reg_home.html', context=context)


def add_plant(request):
    if request.method == 'POST':
        form = AddPlantForm(request.POST, request.FILES)  # Include request.FILES
        if form.is_valid():
            plant = form.save()
            data = DataTable(plant=plant)
            data.save()
            messages.success(request, 'Plant Added Successfully!!!')
            return redirect('index')
        else:
            messages.error(request, 'Invalid Form')
            print(form.errors)  # Print the form errors
    else:
        form = AddPlantForm()
    context = {
        'form': form,
    }
    return render(request, 'add_plant.html', context)
