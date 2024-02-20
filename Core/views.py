from datetime import datetime, timedelta
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from Core.forms import AddPlantForm, EditPlantForm
from Core.models import Plant, DataTable, Sensor
from accounts.models import SiteProfile
import json
import json
import plotly.graph_objs as go
import plotly
from django.utils import timezone
import pytz

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
    if request.user.is_authenticated:

        plants = Plant.objects.filter(user=request.user)
        plant_names = [plant.name.replace(" ", "_") for plant in plants]
        data = {}
        detail_data = {}
        last_24_hours_ago = datetime.now() - timedelta(hours=1000)
        #for creating interactive plot
        plots = []  # To store Plotly plot JSON for each plant
        local_tz = pytz.timezone('America/Los_Angeles')
        for plant in plants:
            # Assuming you have date_time and m_moist or similar data for plotting
            plant_data = DataTable.objects.filter(plant=plant, date_time__gte=last_24_hours_ago)
            if plant_data.exists():
                # Preparing data for Plotly
                dates = [data.date_time.astimezone(local_tz) for data in plant_data]
                values = [data.m_moist for data in plant_data]

                # Creating Plotly figure
                fig = go.Figure(data=[go.Scatter(x=dates, y=values, mode='lines+markers', name=plant.name)]) # accepting a list of dates and values to create chart
                fig.update_layout(title=f"{plant.name} Moisture Over Time", xaxis_title="Date Time",
                                  yaxis_title="Moisture")

                # Convert plot to JSON
                plot_json = plotly.io.to_json(fig) #converts plot into json format
                plots.append(plot_json) #appends each chart for every plant into the list off plots
                print(plot_json, 'Chart')
        latest_data = []
        detailed_data_plots = []
        for plant in plants:
            plant_dict = {}
            plant_data = DataTable.objects.filter(plant=plant, date_time__gte=last_24_hours_ago)
            ec_exists = DataTable.objects.filter(plant=plant).exclude(m_ec__isnull=True).exists()
            print()
            if ec_exists:
                latest_ec_data = DataTable.objects.filter(plant=plant).exclude(m_ec__isnull=True).latest('date_time')
                print(latest_ec_data, 'Latest EC Data')
                plant_dict['latest_ec'] = latest_ec_data.m_ec
                plant_dict['latest_ph'] = latest_ec_data.m_ph
                plant_dict['latest_nitrogen'] = latest_ec_data.m_nitrogen
                plant_dict['latest_m_phosphorus'] = latest_ec_data.m_phosphorus
                plant_dict['latest_potassium'] = latest_ec_data.m_potassium
                plant_dict['latest_temp'] = latest_ec_data.m_temp
                plant_dict['latest_moist'] = latest_ec_data.m_moist
            else:
                plant_dict['latest_ec'] = None
                plant_dict['latest_ph'] = None
                plant_dict['latest_nitrogen'] = None
                plant_dict['latest_phosphorus'] = None
                plant_dict['latest_potassium'] = None
                plant_dict['latest_temp'] = None
                plant_dict['latest_moist'] = None
            plant_dict['name'] = plant.name
            latest_data.append(plant_dict)

            data_key = plant.name.replace(" ", "_")
            data[data_key] = {'date_time':[], 'm_moist':[]}

            for plant_data_item in plant_data:
                if plant_data_item.m_moist is not None:
                    data[data_key]['date_time'].append(plant_data_item.date_time.isoformat())
                    data[data_key]['m_moist'].append(plant_data_item.m_moist)
            # data[data_key]['date_time'] = [plant_data_item.date_time.isoformat() for plant_data_item in plant_data]
            # data[data_key]['m_moist'] = [plant_data_item.m_moist for plant_data_item in plant_data]
            # For more detailed data
            detail_data[data_key] = {}
            detail_data[data_key]['date_time'] = [plant_data_item.date_time.astimezone(local_tz).isoformat() for plant_data_item in plant_data]
            detail_data[data_key]['m_temp'] = [plant_data_item.m_temp for plant_data_item in plant_data]
            detail_data[data_key]['m_ec'] = [plant_data_item.m_ec for plant_data_item in plant_data]
            detail_data[data_key]['m_nitrogen'] = [plant_data_item.m_nitrogen for plant_data_item in plant_data]
            detail_data[data_key]['m_phosphorus'] = [plant_data_item.m_phosphorus for plant_data_item in plant_data]
            detail_data[data_key]['m_potassium'] = [plant_data_item.m_potassium for plant_data_item in plant_data]
            detail_data[data_key]['m_ph'] = [plant_data_item.m_ph for plant_data_item in plant_data]
            detail_plots = []
#             '('potato', {'date_time': ['2024-02-11T04:51:25+00:00', '2024-02-11T04:51:34+00:00', '2024-02-11T04:52:00+00:00', '2024-02-11T04:52:08+00:00', '2024-02-15T03:48:04+00:00'], 'm_temp': [None, None, None, None, 1.0], 'm_ec': [None, None, None, None, 3.0], 'm_nitrogen': [None, None, None, None, 4.0], 'm_phosphorus': [None, None, None, None, 5.0], 'm_potassium': [None, None, None, None, 6.0], 'm_ph': [None, None, None, None, 7.0]}) PLANT
# '
        for plant in detail_data.items():
            plot_data = plant[1]
            print(plant[0])
            print(plot_data, 'PLOT DATA')
            date_time = plot_data['date_time']
            plot_data.pop('date_time')
            print(date_time, 'TIMEE')
            print(plot_data, 'PLOT DATAA')
            for k, v in plot_data.items():
                fig = go.Figure(data=[go.Scatter(x=date_time, y=v, mode='lines+markers', name=plant[0])]) # accepting a list of dates and values to create chart
                fig.update_layout(title=k, xaxis_title="Date Time", yaxis_title=k)
                plot_json = plotly.io.to_json(fig)  # converts plot into json format
                print(plot_json, "PPLOT")
                detail_plots.append(plot_json)  # appends each chart for every plant into the list off plots


        plant_ids = [plant.id for plant in plants]
        print(data, "DATA")
        print(detail_data, "DDATA")
        plant_temperatures = [plant.temperature for plant in plants]
        context = {'plants': plants, 'names': plant_names, 'temps': plant_temperatures, 'profile': profile,
                   'data': json.dumps(data), 'latest_data': json.dumps(latest_data), 'detail_data': json.dumps(detail_data),
                   "ids": json.dumps(plant_ids), 'detail_plots': detail_plots
                   }
    else:
        context = {'profile': profile}
    context.update({'plots': plots})
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
        plant = Plant(user=request.user, name=name, photo=pic, ec=ec, ph=ph, nitrogen=nitrogen, potassium=potassium,
                      phosphorus=phosphorus, temperature=temp, ideal_moisture=ideal_moist, fertilizer=fertilizer,
                      plant_coefficient=plant_coefficient)
        plant.save()
        return redirect('reg_index')


def update_plant_c(request, plant_id):
    print('UPDATING PLANT')
    if request.method == "POST":
        print(request.POST, 'BBBBBBBBBBBBBH')
        plant = Plant.objects.get(pk=plant_id)
        plant.ec = request.POST['ec']
        plant.ph = request.POST['ph']
        plant.nitrogen = request.POST['nitrogen']
        plant.phosphorus = request.POST['phosphorus']
        plant.potassium = request.POST['potassium']
        plant.temperature = request.POST['temperature']
        plant.ideal_moisture = request.POST['ideal_moisture']
        plant.fertilizer = request.POST['fertilizer']
        plant.save()
        print(plant.fertilizer, 'FERTILIZER')
        print(plant.ideal_moisture, request.POST, 'Ideal_temp')
        return redirect('reg_index')

    return JsonResponse({'status': 'error'})


def delete_plant(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)
    if request.user != plant.user:
        return redirect('reg_index')
    plant.delete()
    messages.success(request, 'Plant Deleted!!!')
    return redirect('reg_index')


def add_sensor(request, plant_id=None):
    if request.method == 'POST':
        sensor_user = request.user
        sensor_pin = request.POST.get('sensor_pin')
        sensor_type = request.POST.get('sensor_type')
    if plant_id is not None:
        plant = get_object_or_404(Plant, id=plant_id)
        sensor = Sensor(user=sensor_user, plant=plant, sensor_pin=sensor_pin)
        sensor.save()
        messages.success(request, 'Sensor Saved!!!!!!!!')
        return redirect('reg_index')
    else:
        pass

