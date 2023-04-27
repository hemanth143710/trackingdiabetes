from django.db import models

# Create your models here.
from django.db import models
from authentication.models import User

class BloodSugarLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
    date = models.DateField()
    blood_sugar_am_time = models.TimeField(null=True, blank=True)
    blood_sugar_am_level = models.FloatField(null=True, blank=True)
    breakfast_menu = models.CharField(max_length=255, null=True, blank=True)
    breakfast_time = models.TimeField(null=True, blank=True)
    lunch_menu = models.CharField(max_length=255, null=True, blank=True)
    lunch_time = models.TimeField(null=True, blank=True)
    dinner_menu = models.CharField(max_length=255, null=True, blank=True)
    dinner_time = models.TimeField(null=True, blank=True)
    blood_sugar_pm_time = models.TimeField(null=True, blank=True)
    blood_sugar_pm_level = models.FloatField(null=True, blank=True)