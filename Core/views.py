from datetime import datetime, timedelta
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from Core.forms import AddPlantForm, EditPlantForm
from Core.models import Plant, DataTable, Sensor
from accounts.models import SiteProfile
import json
from plotly.offline import plot
import plotly.graph_objs as go
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
    local_tz = pytz.timezone('America/Los_Angeles')
    profile = SiteProfile.objects.all().first()
    if request.user.is_authenticated:

        plants = Plant.objects.filter(user=request.user)
        sensors = Sensor.objects.filter(user=request.user)
        plant_names = [plant.name.replace(" ", "_") for plant in plants]
        data = {}
        detail_data = {}
        latest_data = []
        for plant in plants:
            plant_dict = {}
            plant_data = DataTable.objects.filter(plant=plant)
            ec_exists = DataTable.objects.filter(plant=plant).exclude(m_ec__isnull=True).exists()
            if ec_exists:
                latest_ec_data = DataTable.objects.filter(plant=plant).exclude(m_ec__isnull=True).latest('date_time')
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
            data[data_key] = {}
            data[data_key]['date_time'] = [plant_data_item.date_time.isoformat() for plant_data_item in plant_data]
            data[data_key]['m_moist'] = [plant_data_item.m_moist for plant_data_item in plant_data]
            # For more detailed data
            detail_data[data_key] = {}
            detail_data[data_key]['date_time'] = [plant_data_item.date_time.isoformat() for plant_data_item in
                                                  plant_data]
            print(detail_data['potato']['date_time'], 'date')
            detail_data[data_key]['m_temp'] = [plant_data_item.m_temp for plant_data_item in plant_data]
            detail_data[data_key]['m_ec'] = [plant_data_item.m_ec for plant_data_item in plant_data]
            detail_data[data_key]['m_nitrogen'] = [plant_data_item.m_nitrogen for plant_data_item in plant_data]
            detail_data[data_key]['m_phosphorus'] = [plant_data_item.m_phosphorus for plant_data_item in plant_data]
            detail_data[data_key]['m_potassium'] = [plant_data_item.m_potassium for plant_data_item in plant_data]
            detail_data[data_key]['m_ph'] = [plant_data_item.m_ph for plant_data_item in plant_data]
        plant_ids = [plant.id for plant in plants]
        plant_temperatures = [plant.temperature for plant in plants]
        plotly_plots = {}
        print(detail_data['potato']['date_time'], 'date1')
        for plant in detail_data.items():
            plot_data = plant[1]
            # print(plant, 'DAPLANt')
            # print(plot_data, 'PLOT DATA')
            date_time = plot_data['date_time']
            print(date_time, 'date_time')
            date_time = [(datetime.strptime(data, "%Y-%m-%dT%H:%M:%S%z")).astimezone(local_tz) for data in date_time]
            # plot_data.pop('date_time')

            # print(date_time, 'TIMEE')
            # print(plot_data, 'PLOT DATAA')
            plant_name = plant[0]
            plotly_plots[plant_name] = {}
            for k, v in plot_data.items():
                if k == 'date_time':
                    continue
                print(k)
                fig = go.Figure(layout=go.Layout(width=525, height=700))
                fig.update_layout(
                    title={
                        'text': k,
                        'y': 0.9,
                        'x': 0.5,
                        'xanchor': 'center',
                        'yanchor': 'top',
                    },
                )
                now = datetime.now()
                fig.update_layout(
                    updatemenus=[
                        dict(
                            type="buttons",
                            direction="right",
                            buttons=list([
                                dict(
                                    args=[{"xaxis.range": [now - timedelta(days=1), now]}],
                                    label="Last Day",
                                    method="relayout"
                                ),
                                dict(
                                    args=[{"xaxis.range": [now - timedelta(days=30), now]}],
                                    label="Last Month",
                                    method="relayout"
                                ),
                                dict(
                                    args=[{"xaxis.range": [now - timedelta(days=365), now]}],
                                    label="Last Year",
                                    method="relayout"
                                ),
                            ]),
                            pad={"r": 1, "t": 1},
                            showactive=True,
                            x=0,
                            xanchor="left",
                            y=.95,
                            yanchor="top"
                        )
                    ]
                )
                fig.update_layout(
                    autosize=False,
                    width=500,
                    height=500,
                    margin=dict(
                        l=10,
                        r=20,
                        b=50,
                        t=50,
                        pad=4
                    )
                )

                scatter = go.Scatter(x=date_time, y=v, mode='lines+markers', name=plant_name, opacity=0.8, marker_color='#e7cd78')
                fig.add_trace(scatter)
                plot_div = plot(fig, output_type='div', include_plotlyjs=False, image_width=200)
                plotly_plots[plant_name].update({k : plot_div})

        print(data, 'data')
        m_moist_graphs = {}
        for plant_name, v in data.items():
            for k, va in v.items():
                if k == 'date_time':
                    dates = va
                    dates = [(datetime.strptime(data, "%Y-%m-%dT%H:%M:%S%z")).astimezone(local_tz) for data in dates]
                if k == 'm_moist':
                    m_moist = va
            fig = go.Figure(layout=go.Layout(width=525, height=700))
            fig.update_layout(
                autosize=False,
                width=700,
                height=412,
                margin=dict(
                    l=10,
                    r=10,
                    b=00,
                    t=40,
                    pad=4
                )
            )
            fig.update_layout(
                title='m_moist Data',
                plot_bgcolor='rgba(245, 241, 237, 1)',
                paper_bgcolor='rgba(0, 0, 0, 0)',
                updatemenus=[
                    dict(
                        type="buttons",
                        direction="right",
                        buttons=list([
                            dict(
                                args=[{"xaxis.range": [now - timedelta(days=1), now]}],
                                label="Last Day",
                                method="relayout"
                            ),
                            dict(
                                args=[{"xaxis.range": [now - timedelta(days=30), now]}],
                                label="Last Month",
                                method="relayout"
                            ),
                            dict(
                                args=[{"xaxis.range": [now - timedelta(days=365), now]}],
                                label="Last Year",
                                method="relayout"
                            ),
                        ]),
                        pad={"r": 1, "t": 1},
                        showactive=True,
                        x=0,
                        xanchor="left",
                        y=1,
                        yanchor="top"
                    )
                ]
            )
            fig.update_xaxes(
                gridcolor='lightgrey',
                ticks='outside',
                mirror=True,
                linecolor='#252323'
            )
            fig.update_yaxes(
                gridcolor='lightgrey',
                ticks='outside',
                mirror=True,
                linecolor='#252323'
            )
            scatter = go.Scatter(x=dates, y=m_moist, mode='lines+markers', name=plant_name, opacity=0.8, marker_color='#e7cd78')
            fig.add_trace(scatter)
            plot_div = plot(fig, output_type='div', include_plotlyjs=False, image_width=200)
            m_moist_graphs[plant_name] = plot_div
        print(m_moist_graphs)
        context = {'plants': plants, 'names': plant_names, 'temps': plant_temperatures, 'profile': profile,
                   'data': json.dumps(data), 'latest_data': latest_data, 'detail_data': json.dumps(detail_data),
                   "ids": json.dumps(plant_ids),'plotly_plots' : plotly_plots, 'm_moist_graphs' : m_moist_graphs, 'sensor' : sensors
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
