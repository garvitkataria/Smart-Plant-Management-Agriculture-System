import uuid
from django.db import models
from plants.models import Plant

# Create your models here.
class Sensor(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    parent = models.ForeignKey(Plant, on_delete=models.CASCADE, null=True)
    sensor_types = (
        ('WL', 'Water Level'),
        ('Temp', 'Temperature'),
        ('SM', 'Soil Moisture'),
        ('HDT', 'Humidity'),
        ('RS', 'RainSensor'),
        ('LDR', 'SunlightSensor')
    )
    sensor_type = models.CharField(max_length=20, choices=sensor_types, default='Temp')
    add_time = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return str(self.id) + " ( " + self.sensor_type + " )"

class Actuator(models.Model):
    name = models.CharField(max_length=10)
    state = models.IntegerField()
    parent = models.ForeignKey(Plant, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

class SensorData(models.Model):
    parent = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    value = models.FloatField(default=0.00)
    read_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.parent.__str__() + " ===> " + str(self.value)
