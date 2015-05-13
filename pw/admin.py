from django.contrib import admin
from pw.models import Meter, HandicappedMeter, MotorcycleMeter, UserProfile, RoadConstruction, LatLong
from pw.models import MeterRating, HandimeterRating, MotometerRating

admin.site.register(UserProfile)
admin.site.register(Meter)
admin.site.register(HandicappedMeter)
admin.site.register(MotorcycleMeter)
admin.site.register(RoadConstruction)
admin.site.register(LatLong)
admin.site.register(MeterRating)
admin.site.register(HandimeterRating)
admin.site.register(MotometerRating)
