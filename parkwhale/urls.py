from django.conf.urls import patterns, include, url
from django.contrib import admin
from pw import views

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'$^', views.index, name="Park Whale"),
    url(r'^about/$', views.about, name="About Us"),
    url(r'^register/$', views.register, name="Park Whale"),
    url(r'^meter_request/$', views.meter_request, name="meter request"),
    url(r'^handimeter_request/$', views.handimeter_request, name="handicap meter request"),
    url(r'^motometer_request/$', views.motometer_request, name="motorcycle meter request"),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^favs/$', views.fav_meters_page, name="Favourite Spots"),
    url(r'^add_fav_meter/$', views.add_fav_meter, name="add fav spot"),
    url(r'^remove_fav_meter/$', views.remove_fav_meter, name="remove fav spot"),
    url(r'^fav_meter_names/$', views.get_fav_meters, name="get fav meters names"),
    url(r'^fav_handimeter_names/$', views.get_fav_handimeters, name="get fav handicap meters names"),
    url(r'^fav_motometer_names/$', views.get_fav_motometers, name="get fav motorcycle meters names"),
    url(r'^rate_meter/$', views.rate_meter, name='update meter rating'),
    url(r'^get_user_rating/$', views.get_user_rating, name="get user meter rating"),
    url(r'^regular/meter/(?P<meter_name>[\w\-]+)/$', views.regmeter, name='Regular Meter Spot'),
    url(r'^handicap/meter/(?P<meter_name>[\w\-]+)/$', views.handimeter, name='Handicap Meter Spot'),
    url(r'^motorcycle/meter/(?P<meter_name>[\w\-]+)/$', views.motometer, name='Motorcycle Meter Spot'),
    url(r'^closure_request/$',views.closure_request, name='closure request'),
)
