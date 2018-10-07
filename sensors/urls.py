from django.conf.urls import url
from .views import add_sensor_data, add_sensor
app_name = 'sensors'
urlpatterns = [
    url(r'^adddata/$', add_sensor_data, name='addsensordata'),
    url(r'^add/$', add_sensor, name='addsensor')
]