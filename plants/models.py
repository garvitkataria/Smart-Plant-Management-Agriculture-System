from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.
class Plant(models.Model):
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    parent = models.ForeignKey(User, on_delete=models.CASCADE)
    alias  = models.CharField(max_length=20, default=None, null=True, blank=True)
    lat = models.FloatField(default = 13.5115)
    lon = models.FloatField(default = 80.0144)

    def __str__(self):
        if self.alias:
            return self.alias
        return str(self.id)

    def get_absolute_url(self):
        return "/plant" +  "/"+ str(self.alias)
