from django.conf.urls import url
from . import views

app_name='auth_part'

urlpatterns = [
    url(r'^newuser/$', views.create_profile, name='createprofile'),
    url(r'^$', views.login, name='login'),
    url(r'^logout/', views.logout_view, name='logout'), #directly logging out by importing logout in view and using it here.   
]