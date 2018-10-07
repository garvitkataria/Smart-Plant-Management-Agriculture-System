from django.contrib import admin
from .models import Sensor, SensorData, Actuator

# Register your models here.
admin.site.register([Sensor, SensorData, Actuator])
