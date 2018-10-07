from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import SensorData, Sensor, Actuator
from plants.models import Plant
from django.core.urlresolvers import reverse


# Create your views here.
@csrf_exempt
def add_sensor_data(request):
    if request.method == 'POST':
        if request.POST.get('abc'):
            act = Actuator.objects.get(name=request.POST.get('name'))
            act.state = request.POST.get('value')
            act.save()
            return HttpResponse(status=200)
        else:
            sID = request.POST.get('sID')
            value = request.POST.get('value')
            if sID and value:
                try:
                    sensor = Sensor.objects.get(id=sID)
                    new_data = SensorData()
                    new_data.parent = sensor
                    new_data.value = value
                    new_data.save()
                    return HttpResponse(status=200)
                except Exception:
                    pass
    return HttpResponse(status=400)

@login_required(login_url='/')
@csrf_exempt
def add_sensor(request):
    if request.method == 'POST':
        data = request.POST
        print(data)
        sensor = Sensor()
        if data.get('alias') and data.get('type'):
            plant = Plant.objects.get(alias=data.get('alias'), parent=request.user)
            print(plant)
            sensor.parent = plant
            sensor.sensor_type = data.get('type')
            sensor.save()
            sensors = plant.sensor_set.all()
            print(sensors)
            temp_sensor = sensors.filter(sensor_type='Temperature')[0]
            hum_sensor = sensors.filter(sensor_type='Humidity')[0]
            moisture_sensor = sensors.filter(sensor_type='Soil Moisture')[0]
            wl_sensor = sensors.filter(sensor_type='Water Level')[0]
            sensor_data_temp = SensorData.objects.filter(parent=temp_sensor)
            sensor_data_hum = SensorData.objects.filter(parent=hum_sensor)
            sensor_data_wlevel = SensorData.objects.filter(parent=wl_sensor)
            sensor_data_mois = SensorData.objects.filter(parent=moisture_sensor)
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
            context={'plant': plant,
            'sensors':sensors,
            'temp': temp,
            'humidity': hum,
            'moisture': mois,
            'wlevel': wlevel,
            }
            return render(request, "plant1.html", context=context)
            return render(request, 'plant1.html', context={'plant': plant, 'id': sensor.id, 'type':sensor.sensor_type})
    return HttpResponseRedirect(reverse('plants:dashboard'))

