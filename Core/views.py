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
    plants = Plant.objects.all()
    # data = DataTable.objects.filter(plant = )
    plant_names = [plant.name for plant in plants]
    data = {}
    for plant in plants:
        plant_data = DataTable.objects.filter(plant=plant)
        print(plant_data, 'plant_name')
        print(data, 'data')
        print(plant, 'plant')
        data[plant.name] = {}
        data[plant.name]['date_time'] = [plant.date_time.isoformat() for plant in plant_data]
        data[plant.name]['m_moist'] = [plant.m_moist for plant in plant_data]
    plant_temperatures = [plant.temperature for plant in plants]
    print(data)
    context = {'plants': plants, 'names': plant_names, 'temps': plant_temperatures, 'profile': profile, 'data':data}
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
