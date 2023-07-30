from datetime import datetime, timedelta
from django.contrib import messages
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


def reg_index(request):
    s_x = [10,15,23,3,12]
    s_y = [1,2,3,4,5]
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
            detail_data[data_key]['date_time'] = [plant_data_item.date_time.isoformat() for plant_data_item in plant_data]
            detail_data[data_key]['m_temp'] = [plant_data_item.m_temp for plant_data_item in plant_data]
            detail_data[data_key]['m_ec'] = [plant_data_item.m_ec for plant_data_item in plant_data]
            detail_data[data_key]['m_npk'] = [plant_data_item.m_npk for plant_data_item in plant_data]
            detail_data[data_key]['m_ph'] = [plant_data_item.m_ph for plant_data_item in plant_data]
        plant_ids = [plant.id for plant in plants]
        print('DETAIL DATA')
        print(detail_data)
        print('DATA')
        print(data)

        print('LATEST DATA')
        print(latest_data)
        plant_temperatures = [plant.temperature for plant in plants]
        context = {'plants': plants, 'names': plant_names, 'temps': plant_temperatures, 'profile': profile,
                   'data': json.dumps(data), 'latest_data': latest_data, 'detail_data': json.dumps(detail_data),
                   "ids": json.dumps(plant_ids), 's_x':s_x, 's_y':s_y,
                   }
    else:
        context={'profile':profile}
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
    else:
        form = AddPlantForm()
    context = {
        'form': form,
    }
    return render(request, 'add_plant.html', context)


def plant_details(request, plant_id):
    profile = SiteProfile.objects.all().first()
    plant = get_object_or_404(Plant, pk= plant_id)
    plant_dict = {}
    detail_data = {}
    last_24_hours_ago = datetime.now() - timedelta(hours=500)
    latest_data = []
    plant_data = DataTable.objects.filter(plant=plant, date_time__gte=last_24_hours_ago)
    latest_ec_data = DataTable.objects.filter(plant=plant).exclude(m_ec__isnull=True).latest('date_time')
    plant_dict['latest_ec'] = latest_ec_data.m_ec
    plant_dict['latest_ph'] = latest_ec_data.m_ph
    plant_dict['latest_npk'] = latest_ec_data.m_npk
    plant_dict['latest_temp'] = latest_ec_data.m_temp
    plant_dict['latest_moist'] = latest_ec_data.m_moist
    plant_dict['name'] = plant.name
    print(plant_dict,'PLANT DICT')
    # For more detailed data

    detail_data = {}
    plant_fields = ['m_temp', 'm_ec', 'm_npk', 'm_ph']
    r_date_time = [plant_data_item.date_time.isoformat() for plant_data_item in plant_data]
    formatted_timestamps = []

    for ts in r_date_time:
        dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        dt_dict = {
            'year': dt.year,
            'month': dt.month,
            'day': dt.day,
            'hour': dt.hour,
            'minute': dt.minute,
        }
        formatted_timestamps.append(dt_dict)
        datetime_hours = [t['hour'] for t in formatted_timestamps]
        print(datetime_hours, 'DATETIME HOURS')
    print(formatted_timestamps, 'FORMATTED TIME STAMPS')
    detail_data['m_temp'] = [plant_data_item.m_temp for plant_data_item in plant_data]
    detail_data['m_ec'] = [plant_data_item.m_ec for plant_data_item in plant_data]
    detail_data['m_npk'] = [plant_data_item.m_npk for plant_data_item in plant_data]
    detail_data['m_ph'] = [plant_data_item.m_ph for plant_data_item in plant_data]
    print(detail_data, 'DETAIL DATA')
    print(r_date_time, 'RECORDED DATE TIME')
    context={
        'latest_data':json.dumps(plant_dict),
        'detail_data':json.dumps(detail_data),
        'r_date_time':r_date_time,
        'p_fields':plant_fields,
        'plant':plant,
        'profile': profile,
        'f_time': json.dumps(formatted_timestamps),
        'hours': datetime_hours
    }
    return render(request, 'Core/reg_home.html', context=context)


def edit_plant_form(request, plant_id):
    profile = SiteProfile.objects.all().first()
    plant = Plant.object.get(id = plant_id)
    if request.method == 'POST':
        form = EditPlantForm(request.POST, instance=plant)
        if form.is_valid():
            form.save()
            return redirect('reg_index')
        else:
            messages.error('Form Not Valid!!!')

    else:
        form = EditPlantForm(instance=plant)
    context = {'form': form, 'profile':profile}
    return render(request,'Core/reg_home.html', context=context)