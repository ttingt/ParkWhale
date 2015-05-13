from django.shortcuts import render
from pw.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from pw.models import Meter, HandicappedMeter, MotorcycleMeter, LatLong, RoadConstruction, UserProfile, MeterRating, HandimeterRating, MotometerRating
from django.db.models import Q
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
import json

def index(request):
    return render(request, 'pw/index.html', {})

def about(request):
    return render(request, 'pw/about.html', {})

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            registered = True
        else:
            print user_form.errors, profile_form.errors

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,
            'pw/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})

def meter_request(request):
    if request.method == 'GET':
        lat = request.GET['latitude']
        lng = request.GET['longitude']
        nearbyMeters = get_meters_near(float(lat), float(lng))
        meterRatings = {}
        for nm in nearbyMeters:
            meterRatings[str(nm.name)] = get_meter_rating(nm.name, nm.type)
        data = queried_meters_data_to_json(nearbyMeters)
        ratings = json.dumps(meterRatings)
        return HttpResponse('[{"meters": ' + data + ', "ratings": ' + ratings + "}]")
    else:
        return HttpResponse("Data error")

def handimeter_request(request):
    if request.method == 'GET':
        lat = request.GET['latitude']
        lng = request.GET['longitude']
        nearbyMeters = get_handimeters_near(float(lat), float(lng))
        meterRatings = {}
        for nm in nearbyMeters:
            meterRatings[str(nm.name)] = get_meter_rating(nm.name, nm.type)
        data = queried_meters_data_to_json(nearbyMeters)
        ratings = json.dumps(meterRatings)
        return HttpResponse('[{"meters": ' + data + ', "ratings": ' + ratings + "}]")
    else:
        return HttpResponse("Data error")

def motometer_request(request):
    if request.method == 'GET':
        lat = request.GET['latitude']
        lng = request.GET['longitude']
        nearbyMeters = get_motometers_near(float(lat), float(lng))
        meterRatings = {}
        for nm in nearbyMeters:
            meterRatings[str(nm.name)] = get_meter_rating(nm.name, nm.type)
        data = queried_meters_data_to_json(nearbyMeters)
        ratings = json.dumps(meterRatings)
        return HttpResponse('[{"meters": ' + data + ', "ratings": ' + ratings + "}]")
    else:
        return HttpResponse("Data error")

def closure_request(request):
    if request.method == "GET":
        lat = request.GET['latitude']
        lng = request.GET['longitude']
        nearbyClosures = get_closures_near(float(lat), float(lng))
        data = queried_meters_data_to_json(nearbyClosures)
        return HttpResponse(data)
    else:
        return HttpResponse('Data error')

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return HttpResponse('Your user account is inactive!')
        else:
            print 'Invalid login details:{0} - {1} -'.format(username, password)
            return HttpResponse('User login details invalid')
    else:
        return render(request, 'pw/login.html', {})

# FAVOURITE METER ================================================================

@login_required
def fav_meters_page(request):
    user = UserProfile.objects.get(user=request.user)
    data = {'meters':user.favMeters.all(), 'handimeters':user.favHMeters.all(), 'motometers':user.favMMeters.all()}
    return render(request, 'pw/favs.html', data)

def add_fav_meter(request):
    if request.user.is_authenticated():
        user = UserProfile.objects.get(user=request.user)
    else:
        return HttpResponse(False)

    if request.method == 'GET':
        meter_name = request.GET['meter_name']
        meter_type = request.GET['meter_type']
    else:
        return HttpResponse(False)
    added = False
    try:
        if (meter_type == "regular"):
            meter = Meter.objects.get(name=meter_name)
            user.favMeters.add(meter)
        elif (meter_type == "handicap"):
            meter = HandicappedMeter.objects.get(name=meter_name)
            user.favHMeters.add(meter)
        else:
            meter = MotorcycleMeter.objects.get(name=meter_name)
            user.favMMeters.add(meter)
        user.save()
        added = True
    except ObjectDoesNotExist:
        pass
    return HttpResponse(added)

def remove_fav_meter(request):
    if request.user.is_authenticated():
        user = UserProfile.objects.get(user=request.user)
    else:
        return HttpResponse(False)

    if request.method == 'GET':
        meter_name = request.GET['meter_name']
        meter_type = request.GET['meter_type']
    else:
        return HttpResponse(False)
    removed = False
    try:
        if (meter_type == "regular"):
            meter = Meter.objects.get(name=meter_name)
            user.favMeters.remove(meter)
        elif (meter_type == "handicap"):
            meter = HandicappedMeter.objects.get(name=meter_name)
            user.favHMeters.remove(meter)
        else:
            meter = MotorcycleMeter.objects.get(name=meter_name)
            user.favMMeters.remove(meter)
        user.save()
        removed = True
    except ObjectDoesNotExist:
        pass
    return HttpResponse(removed)

# RATE METER ======================================================================

@login_required
def rate_meter(request):
    user = request.user
    meter = meter_name = meter_type = new_rating = rating = False
    if request.method != 'GET':
        return JsonResponse({'msg': "Not a valid request."})
    meter_name = request.GET['meterName']
    meter_type = request.GET['meterType']
    new_rating = request.GET['rate']
    if meter_name:
        if meter_type == "regular":
            meter = Meter.objects.get(name=meter_name)
            if meter:
                try:
                    rating = MeterRating.objects.get(user=user, meter=meter)
                except ObjectDoesNotExist:
                    rating = MeterRating.objects.create(user=user, meter=meter, n=new_rating)
        elif meter_type == "handicap":
            meter = HandicappedMeter.objects.get(name=meter_name)
            if meter:
                try:
                    rating = HandimeterRating.objects.get(user=user, meter=meter)
                except ObjectDoesNotExist:
                    rating = HandimeterRating.objects.create(user=user, meter=meter, n=new_rating)
        elif meter_type == "motorcycle":
            meter = MotorcycleMeter.objects.get(name=meter_name)
            if meter:
                try:
                    rating = MotometerRating.objects.get(user=user, meter=meter)
                except ObjectDoesNotExist:
                    rating = MotometerRating.objects.create(user=user, meter=meter, n=new_rating)
    if meter:
        rating.n = new_rating
        rating.save()
        msg = "Thanks for rating!"
    new_total_rating = get_meter_rating(meter_name, meter_type)
    data = {'msg': msg, 'newRating': new_total_rating}
    return JsonResponse(data)

def get_meter_rating(meter_name, meter_type):
    totalRating = 0
    count = 0
    try:
        if meter_type == "regular":
            meter = Meter.objects.get(name=meter_name)
            ratings = MeterRating.objects.filter(meter=meter)
        elif meter_type == "handicap":
            meter = HandicappedMeter.objects.get(name=meter_name)
            ratings = HandimeterRating.objects.filter(meter=meter)
        else:
            meter = MotorcycleMeter.objects.get(name=meter_name)
            ratings = MotometerRating.objects.filter(meter=meter)
    except ObjectDoesNotExist:
        pass
    for r in ratings:
        totalRating += r.n
        count += 1
    return 0 if (count==0) else totalRating/count

def get_user_rating(request):
    if request.method == 'GET':
        user = request.user
        meter_name = request.GET['meter_name']
        meter_type = request.GET['meter_type']
        try:
            if meter_type == "regular":
                meter = Meter.objects.get(name=meter_name)
                rating = MeterRating.objects.filter(meter=meter, user=user).values_list('n', flat=True)
            elif meter_type == "handicap":
                meter = HandicappedMeter.objects.get(name=meter_name)
                rating = HandimeterRating.objects.filter(meter=meter, user=user).values_list('n', flat=True)
            else:
                meter = MotorcycleMeter.objects.get(name=meter_name)
                rating = MotometerRating.objects.filter(meter=meter, user=user).values_list('n', flat=True)
        except ObjectDoesNotExist:
            rating = 0
        return HttpResponse(rating)
    else:
        return HttpResponse(0)

# METER INFO PAGES ================================================================

def regmeter(request, meter_name):
    context_dict = {}
    context_dict['fav'] = False
    context_dict['rating'] = 0
    try:
        meter = Meter.objects.get(name=meter_name)
        context_dict['meter'] = meter
        rating = get_meter_rating(meter_name, meter.type)
        context_dict['rating'] = rating
    except Meter.DoesNotExist:
        return HttpResponse("This meter, meter #" + meter_name + ", doesn\'t exist!")
    if request.user.is_authenticated():
        user = UserProfile.objects.get(user=request.user)
        if user.favMeters.filter(name=meter_name).exists():
            context_dict['fav'] = True
    return render(request, 'pw/meter.html', context_dict)

def handimeter(request, meter_name):
    context_dict = {}
    context_dict['fav'] = False
    try:
        meter = HandicappedMeter.objects.get(name=meter_name)
        context_dict['meter'] = meter
        rating = get_meter_rating(meter_name, meter.type)
        context_dict['rating'] = rating
    except HandicappedMeter.DoesNotExist:
        return HttpResponse("This meter, meter #" + meter_name + ", doesn\'t exist!")
    if request.user.is_authenticated():
        user = UserProfile.objects.get(user=request.user)
        if user.favHMeters.filter(name=meter_name).exists():
            context_dict['fav'] = True
    return render(request, 'pw/meter.html', context_dict)

def motometer(request, meter_name):
    context_dict = {}
    context_dict['fav'] = False
    try:
        meter = MotorcycleMeter.objects.get(name=meter_name)
        context_dict['meter'] = meter
        rating = get_meter_rating(meter_name, meter.type)
        context_dict['rating'] = rating
    except MotorcycleMeter.DoesNotExist:
        return HttpResponse("This meter, meter #" + meter_name + ", doesn\'t exist!")
    if request.user.is_authenticated():
        user = UserProfile.objects.get(user=request.user)
        if user.favMMeters.filter(name=meter_name).exists():
            context_dict['fav'] = True
    return render(request, 'pw/meter.html', context_dict)

# def roadclosure(request, closure_name):
#     context_dict = {}
#     try:
#         closure = LatLong.objects.get(construction=closure_name)
#         context_dict['closure'] = closure
#     except LatLong.DoesNotExist:
#         pass
#     return render(request, 'pw/closure.html', context_dict)

# METER DATA QUERYING ==============================================================

def get_meters_near(lat, lng):
    args = (Q(lng__range=(lng-0.003,lng+0.003)) & Q(lat__range=(lat-0.003,lat+0.003)))
    meters = Meter.objects.filter(args)
    return meters

def get_handimeters_near(lat, lng):
    args = (Q(lng__range=(lng-0.003,lng+0.003)) & Q(lat__range=(lat-0.002,lat+0.002)))
    handimeters = HandicappedMeter.objects.filter(args)
    return handimeters

def get_motometers_near(lat, lng):
    args = (Q(lng__range=(lng-0.003,lng+0.003)) & Q(lat__range=(lat-0.002,lat+0.002)))
    motormeters = MotorcycleMeter.objects.filter(args)
    return motormeters

def queried_meters_data_to_json(meters):
    data = serializers.serialize('json', meters)
    return data

def get_closures_near(lat, lng):
    args = (Q(x__range=(lat-0.005,lat+0.005)) & Q(y__range=(lng-0.005,lng+0.005)))
    closures = LatLong.objects.filter(args)
    return closures

def get_fav_meters(request):
    user = UserProfile.objects.get(user=request.user)
    data = queried_meters_data_to_json(user.favMeters.all())
    return HttpResponse(data)

def get_fav_handimeters(request):
    user = UserProfile.objects.get(user=request.user)
    data = queried_meters_data_to_json(user.favHMeters.all())
    return HttpResponse(data)

def get_fav_motometers(request):
    user = UserProfile.objects.get(user=request.user)
    data = queried_meters_data_to_json(user.favMMeters.all())
    return HttpResponse(data)
    
# ==================================================================================
