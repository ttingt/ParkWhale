from django.db import models
from django.contrib.auth.models import User

class Meter(models.Model):
    name = models.IntegerField()
    lng = models.FloatField()
    lat = models.FloatField()
    timeOfEffect = models.CharField(max_length=64)
    timeLimit = models.CharField(max_length=64)
    rate = models.CharField(max_length=64)
    type = models.CharField(max_length=64)

    def __unicode__(self):
        return str(self.name)

class HandicappedMeter(models.Model):
    name = models.IntegerField()
    lng = models.FloatField()
    lat = models.FloatField()
    type = models.CharField(max_length=64)

    def __unicode__(self):
        return str(self.name)

class MotorcycleMeter(models.Model):
    name = models.IntegerField()
    lng = models.FloatField()
    lat = models.FloatField()
    type = models.CharField(max_length=64)

    def __unicode__(self):
        return str(self.name)

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    favMeters = models.ManyToManyField(Meter)
    favHMeters = models.ManyToManyField(HandicappedMeter)
    favMMeters = models.ManyToManyField(MotorcycleMeter)

    def __unicode__(self):
        return self.user.username

class RoadConstruction(models.Model):
    num = models.IntegerField(default=0)
    description = models.CharField(max_length=512)
    status = models.CharField(max_length=64)

    def __unicode__(self):
        return str(self.description)

class LatLong(models.Model):
    x = models.FloatField()
    y = models.FloatField()
    construction = models.ForeignKey('RoadConstruction')

    def __unicode__(self):
        return str(self.construction.num)

class MeterRating(models.Model):
    user = models.ForeignKey(User)
    n = models.IntegerField()
    meter = models.ForeignKey(Meter)

class HandimeterRating(models.Model):
    user = models.ForeignKey(User)
    n = models.IntegerField()
    meter = models.ForeignKey(HandicappedMeter)

class MotometerRating(models.Model):
    user = models.ForeignKey(User)
    n = models.IntegerField()
    meter = models.ForeignKey(MotorcycleMeter)