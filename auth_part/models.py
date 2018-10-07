from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
# Create your models here.

'''class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    CHOICES = (
        ('U', 'USER'),
        ('P', 'PLANT'),
    )
    position = models.CharField(
        max_length=2,
        choices=CHOICES,
        default='U',
    )

    def __repr__(self):
        return self.user.username

    def __str__(self):
        return self.user.username
        
'''
class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

'''class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['position']  
'''          

        