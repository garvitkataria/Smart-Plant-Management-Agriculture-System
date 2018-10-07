from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse
from django.forms.models import model_to_dict
from sensors.models import Sensor, SensorData, Actuator


from .models import Plant

# Create your views here.
@login_required(login_url='/')
@csrf_exempt
def add_plant(request):
    if request.method == 'POST':
        plant = Plant()
        if (not request.POST.get('alias')) or len(Plant.objects.filter(alias=request.POST.get('alias')))!=0 :
            return HttpResponseRedirect(reverse('plants:dashboard'))
        plant.alias = request.POST.get('alias')
        plant.parent = request.user
        plant.save()
        sensor1 = Sensor()
        sensor1.sensor_type = 'Temperature'
        sensor1.parent = plant
        sensor1.save()
        sensor2 = Sensor()
        sensor2.sensor_type = 'Humidity'
        sensor2.parent = plant
        sensor2.save()
        sensor3 = Sensor()
        sensor3.sensor_type = 'Soil Moisture'
        sensor3.parent = plant
        sensor3.save()
        sensor4 = Sensor()
        sensor4.sensor_type = 'Water Level'
        sensor4.parent = plant
        sensor4.save()
        sensor5 = Sensor()
        sensor5.parent = plant
        sensor5.sensor_type = 'RainSensor'
        sensor5.save()
        actuator = Actuator()
        actuator.parent = plant
        actuator.name = request.POST.get('alias')
        actuator.state = 0
        actuator.save()

        return HttpResponseRedirect(reverse('plants:dashboard'))
    return HttpResponseRedirect(reverse('plants:dashboard'))

@login_required(login_url='/')
def viewdashboard(request):
    print(request.user)
    plants = Plant.objects.filter(parent=request.user)
    print(plants)
    return render(request, 'userdashboard.html', {'username': request.user.username, 'plants': plants})

@login_required(login_url='/')
def last_readings(request, username):
    print (username)
    plant = Plant.objects.get(alias=username, parent=request.user)
    print(plant.alias)
    sensors = plant.sensor_set.all()
    rain_values = SensorData.objects.filter(parent__sensor_type='RainSensor', parent__parent=plant)[0:100]
    rain_values = list(map(lambda x: model_to_dict(x), rain_values))
    temp_values = SensorData.objects.filter(parent__sensor_type='Temperature', parent__parent=plant)[:100]
    temp_values = list(map(lambda x: model_to_dict(x), temp_values))
    moisture_values = SensorData.objects.filter(parent__sensor_type='Soil Moisture', parent__parent=plant)[:100]
    moisture_values = list(map(lambda x: model_to_dict(x), moisture_values))

    wl_values = SensorData.objects.filter(parent__sensor_type='Water Level', parent__parent=plant)[:100]
    wl_values = list(map(lambda x: model_to_dict(x), wl_values))

    humidity_values = SensorData.objects.filter(parent__sensor_type='Humidity', parent__parent=plant)[:100]
    humidity_values = list(map(lambda x: model_to_dict(x), humidity_values))
    dict1={'temp_values':temp_values,'rain_values':rain_values,'moisture_values':moisture_values,'wl_values':wl_values,'humidity_values':humidity_values}
    return JsonResponse(dict1, safe=False)

@login_required(login_url='/')
def plantboard(request, username):
    print (username)
    plant = Plant.objects.get(alias=username, parent=request.user)
    print(plant.alias)
    sensors = plant.sensor_set.all()
    print(sensors)
    rain_sensor = sensors.filter(sensor_type='RainSensor')[0]
    temp_sensor = sensors.filter(sensor_type='Temperature')[0]
    hum_sensor = sensors.filter(sensor_type='Humidity')[0]
    moisture_sensor = sensors.filter(sensor_type='Soil Moisture')[0]
    wl_sensor = sensors.filter(sensor_type='Water Level')[0]
    sensor_data_temp = SensorData.objects.filter(parent=temp_sensor)
    sensor_data_hum = SensorData.objects.filter(parent=hum_sensor)
    sensor_data_wlevel = SensorData.objects.filter(parent=wl_sensor)
    sensor_data_mois = SensorData.objects.filter(parent=moisture_sensor)
    sensor_data_rain = SensorData.objects.filter(parent=rain_sensor)
    act = Actuator.objects.get(parent__alias=username, name=plant.alias)
    try:
        temp = sensor_data_temp.latest('id')
    except Exception:
        temp = None
    try:
        hum = sensor_data_hum.latest('id')
    except Exception:
        hum = None
    try:
        wlevel = sensor_data_wlevel.latest('id')
    except Exception:
        wlevel = None
    try:
        mois = sensor_data_mois.latest('id')
    except Exception:
        mois = None
    try:
        rain = sensor_data_rain.latest('id')
    except Exception:
        rain = None
    temp_values = list(map(lambda x: x.value, list(sensor_data_temp)[-1:-11:-1]))
    soil_values = list(map(lambda x: x.value, list(sensor_data_mois)[-1:-11:-1]))
    hum_values = list(map(lambda x: x.value, list(sensor_data_hum)[-1:-11:-1]))
    #ldr_values = list(map(lambda x: x.value, list(sensor_data_hum)[-1:-11:-1]))
    rain_values = list(map(lambda x: x.value, list(sensor_data_rain)[-1:-11:-1]))

    context={'plant': plant,
     'sensors':sensors,
     'temp': temp,
     'humidity': hum,
     'moisture': mois,
     'wlevel': wlevel,
     'rain':rain,
     'act': act,
     'temp_values':temp_values[::-1],
     'soil_values':soil_values[::-1],
     'humidity_values': hum_values[::-1],
     'rain_values': rain_values[::-1]
     }
    print(context)
    return render(request, "plant1.html", context=context)
    return HttpResponse(str(id))







