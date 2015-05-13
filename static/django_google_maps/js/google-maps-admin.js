
/*
Integration for Google Maps in the django admin.

NOTE: Code snippets taken from Django-Google-Maps: an open-source script 
 Github: https://github.com/madisona/django-google-maps

<script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script>

*/

function googleMapAdmin() {
    // meter type strings
    var regStr = "regular";
    var handiStr = "handicap";
    var motoStr = "motorcycle";

    var geocoder = new google.maps.Geocoder();
    var map;
    var marker;
    var markerwindow;
    var favMeters = [];
    var favMeterNames = [];
    var favHandimeterNames = [];
    var favMotometerNames = [];
    var markers = [];
    var handimarkers = [];
    var motomarkers = [];
    var closurelines = [];

    var self = {
        // Starts all the processes
        initialize: function() {
            var lat = 49.276698;
            var lng = -123.123934;
            var zoom = 12;

            var latlng = new google.maps.LatLng(lat,lng);
            var myOptions = {
              zoom: zoom,
              center: latlng,
              mapTypeId: google.maps.MapTypeId.ROADMAP
            };
            map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);

            self.addClickToCloseInfoWindows();
            if (loggedIn) self.getFavMeters();
            self.attachHandlers();
            self.showType(closurelines);
        },
        
        // Event handlers attached
        attachHandlers: function() {
            $("#address_button").click(function() {self.codeAddress();});
            $("#id_address").change(function() {self.codeAddress();});
            $("#reg_check").change(function() {
                if($(this).is(':checked')) {
                    self.showType(markers);
                }
                else self.hideType(markers);
            });
            $("#handi_check").change(function() {
                                   if($(this).is(':checked')) {
                                    self.showType(handimarkers);
                                   }
                                    else self.hideType(handimarkers);
                                   });
            $("#moto_check").change(function() {
                                   if($(this).is(':checked')) {
                                    self.showType(motomarkers);
                                   }
                                    else self.hideType(motomarkers);
                                   });
            $("#price_check").change(function() {
                                     self.filterAll();
                                    });
            $("#time_check").change(function() {
                                    if ($(this).val() == "all") {
                                    $("#m_check").hide();
                                    } else {
                                    $("#m_check").show();
                                    }
                                    self.filterAll();
                                    });
            $("#m_check").change(function() {
                                    self.filterAll();
                                 });
            $("#fav_check").change(function() {
                                   if ($(this).is(':checked')) {
                                   self.showType(favMeters);
                                   } else {
                                    self.hideType(favMeters);
                                   }
                                   });
        },
        
        // Event handler to close marker window on click.
        addClickToCloseInfoWindows: function() {
            google.maps.event.addListener(map, 'click', function() {
                if (markerwindow != null) {
                    markerwindow.close();
                    markerwindow = null;
                }
            });
        },
        
        // HTTP GET to add a meter to the favorites list.
        addFavMeter: function(marker, name, type, favButton) {
            $.get('add_fav_meter/', {meter_name: name, meter_type: type}, function(result){
                if (result == "True") {
                    marker.setIcon("static/images/favmeter.png");
                    favButton.value = "<\\3";
                    favMeters.push(marker);
                    marker.setMap(map);
                } else {
                    alert('Please login to favourite spots.');
                }
            });
        },

        // Given some options on lat/lng and draggability, adds a new marker to the map.
        addMarker: function(Options) {
            marker = new google.maps.Marker({
                map: map,
                position: Options.latlng
            });

            var draggable = Options.draggable || false;
            if (draggable) {
                self.addMarkerDrag(marker);
            }
        },
        
        // Sets the marker draggability to true
        addMarkerDrag: function() {
            marker.setDraggable(true);
        },
        
        // For a given marker with given spot data and rating,
        // creates and attaches a window for each spot
        attachWindowMessage: function(marker, spot, rating) {
            var content = document.createElement('div'), favButton;
            content.innerHTML = self.setMarkerWindowText(spot, rating);
            var favButton = self.createFavButton(spot);
            content.appendChild(favButton);

            google.maps.event.addDomListener(favButton, 'click', function(){
                if (favButton.value == "<3") {
                    self.addFavMeter(marker, spot.name, spot.type, favButton);
                } else {
                    self.removeFavMeter(marker, spot.name, spot.type, favButton);
                }
            });

            var infowindow = new google.maps.InfoWindow({
                content: content
            });

            google.maps.event.addListener(marker, 'click', function() {
                if (markerwindow != null) {
                    markerwindow.close();
                }
                markerwindow = infowindow;
                markerwindow.open(marker.get('map'), marker);
            });
        },
        
        // Given a spot name and a type of string,
        // returns an icon associated with that type of spot.
        chooseIcon: function(name, type) {
            var icon;
            if (type == handiStr) {
                icon = "static/images/handilogo.png"
            } else if (type == regStr) {
                icon = "static/images/logo.png";
            } else {
                icon = "static/images/motologo.png";
            }
            return icon;
        },

        // Takes the address written into the input box and codes it into lat/lng
        // and then acts as a master control to plot all relevant data to that lat/lng
        codeAddress: function() {
            var address = $("#id_address").val() + " Vancouver BC";
            geocoder.geocode({'address': address}, function(results, status) {
                if (status == google.maps.GeocoderStatus.OK) {
                    var latlng = results[0].geometry.location;
                    if (latlng.k == 49.2827291 && latlng.D == -123.12073750000002) {
                        alert("Location not found!");
                    } else {
                        map.setCenter(latlng);
                        map.setZoom(17);

                        self.unplotAll();
                        self.setMarker(latlng);
                        self.getMeters(latlng);
                        self.getClosures(latlng);
                    }
                } else {
                    alert("Geocode was not successful for the following reason: " + status);
                }
            });
        },
        
        // Given spot data, decides if spot is a favorite or not
        // and creates a button with the appropriate value
        createFavButton: function(spot) {
            var favButton = document.createElement('input');
            favButton.type = 'button';

            var fav = false;
            if (spot.type == regStr) {
                fav = (favMeterNames.indexOf(spot.name) != -1);
            } else if (spot.type == handiStr) {
                fav = (favHandimeterNames.indexOf(spot.name) != -1);
            } else {
                fav = (favMotometerNames.indexOf(spot.name) != -1);
            }
            if (fav) {
                favButton.value = '<\\3';
            } else {
                favButton.value = '<3';
            }
            return favButton;
        },
        
        // For every marker in the regular spot list, filters by time and price.
        filterAll: function() {
            for (var i = 0; i < markers.length; i++) {
                if (self.filterPrice(markers[i]) && self.filterTime(markers[i]))
                    markers[i].setMap(map);
                else markers[i].setMap(null);
            }
        },
        
        // Given marker data, returns whether or not a spot should be plotted.
        filterPrice: function(marker) {
            return self.isAcceptablePrice(marker.getTitle().split("$")[1].split("*")[0]);
        },
        
        // For a given marker data, returns true if it's time of effect does not
        // include the user's set time.
        filterTime: function(marker) {
            return self.isAcceptableTime(marker.getTitle().split("*")[1]);
        },
        
        // Given a string of info, finds the end time.
        findEndTime: function(info) {
            var endStr = info.split("TO ")[1];
            var m = endStr.split(" ")[1];
            var time = parseFloat(endStr.split(":")[0]);
            if (m == "PM")
                return time+12;
            else return time;
        },
        
        // Given a string of info, extracts the start time
        findStartTime: function(info) {
            var startStr = info.split("EFFECT: ")[1].split(" TO")[0];
            var m = startStr.split(" ")[1];
            var time = parseFloat(startStr.split(":")[0]);
            if (m == "PM")
                return time+12;
            else return time;
        },
        
        //HTTP GET for closure data at given lat/lng
        getClosures: function (latlng){
            $.get('closure_request/', {latitude: latlng.lat(), longitude: latlng.lng()}, function(data){
                var closures = JSON.parse(data);
                self.plotClosures(closures);
            });
        },
        
        // HTTP GET for favorite meters
        // Favorite Meters added to global arrays
        getFavMeters: function() {
            favMeters = [];
            $.get('fav_meter_names/', {}, function(data){
                var meters = JSON.parse(data);
                for (var i=0; i<meters.length; i++) {
                    favMeterNames.push(meters[i].fields.name);
                    self.pushFavMeter(meters[i]);
                }
            });
            $.get('fav_handimeter_names/', {}, function(data){
                var meters = JSON.parse(data);
                for (var i=0; i<meters.length; i++) {
                    favHandimeterNames.push(meters[i].fields.name);
                    self.pushFavMeter(meters[i]);
                }
            });
            $.get('fav_motometer_names/', {}, function(data){
                var meters = JSON.parse(data);
                for (var i=0; i<meters.length; i++) {
                    favMotometerNames.push(meters[i].fields.name);
                    self.pushFavMeter(meters[i]);
                }
            });
        },
        
        // HTTP GET for meter data.
        // Pushes meter to arrays.
        getMeters: function(latlng) {
            $.get('meter_request/', {latitude: latlng.lat(), longitude: latlng.lng()}, function(data){
                  var results = JSON.parse(data);
                  spots = results[0].meters;
                  ratings = results[0].ratings;
                  self.plotSpots(spots, ratings);
                  });
            $.get('handimeter_request/', {latitude: latlng.lat(), longitude: latlng.lng()}, function(data) {
                  var results = JSON.parse(data);
                  spots = results[0].meters;
                  ratings = results[0].ratings;
                  self.plotSpots(spots, ratings);
                  });
            $.get('motometer_request/', {latitude: latlng.lat(), longitude: latlng.lng()}, function(data) {
                  var results = JSON.parse(data);
                  spots = results[0].meters;
                  ratings = results[0].ratings;
                  self.plotSpots(spots, ratings);
                  });
        },
        
        // Gets the relevant time in 24 hour time.
        getTime: function() {
            if ($("#time_check").val() == "all")
                return;
            if ($("#m_check").val() == 2)
                return parseFloat($("#time_check").val()) + 12;
            else return parseFloat($("#time_check").val());
        },
        
        // Hides every marker in marklist.
        hideType: function(marklist) {
            self.setAllMap(null, marklist);
        },
        
        // Given a price, returns true if our price is within the user's set range.
        isAcceptablePrice: function(price) {
            return price <= $("#price_check").val();
        },
        
        // For a given time of effect,
        // decides whether the user's given time is outside of the range.
        isAcceptableTime: function(toe) {
            if ($("#time_check").val() == "all")
                return true;
            var start = self.findStartTime(toe);
            var end = self.findEndTime(toe);
            var target = self.getTime();
            return self.isOutOfTimeRange(start, end, target);
        },
        
        // Given a start time, end time, and target time, decides whether the target
        // time is outside of the start-end time range.
        isOutOfTimeRange: function(start, end, time) {
            if (end - start < 0) {
                return (time > end && time < start);
            } else if (end - start > 0) {
                return (time < start || time > end);
            } else return false;
        },
        
        // Given closure data, plots closures on the map.
        // There is a rectangular and polyline representation.
        plotClosures: function(closures){

            /* //FOR RECTANGULAR REPRESENTATION OF CONSTRUCTION

            var min;
            var max;
            var minx;
            var maxx;
            var miny;
            var maxy;

            if (closures.length > 0){
                min = closures[0];
                max = closures[0];
                minx = closures[0].fields.x;
                maxx = closures[0].fields.x;
                miny = closures[0].fields.y;
                maxy = closures[0].fields.y;
            }


            for (var l = 0; l < closures.length; l++){
                
                if (minx == maxx && miny == maxy && closures[l+1].fields.construction != min.fields.construction){
                    var marker = new google.maps.Marker({
                        position: new google.maps.LatLng(closures[l].fields.x, closures[l].fields.y),
                        map: map,
                        icon: 'static/images/handispot.png'
                    });
                }

                if (closures[l].fields.construction != max.fields.construction || l + 1 == closures.length){
                    var rectangle = new google.maps.Rectangle({
                        strokeColor: '#FF0000',
                        strokeOpacity: 0.8,
                        strokeWeight: 2,
                        fillColor: '#FF0000',
                        fillOpacity: 0.35,
                        map: map,
                        bounds: new google.maps.LatLngBounds(
                                    new google.maps.LatLng(minx, miny),
                                    new google.maps.LatLng(maxx, maxy))
                        });
                    min = closures[l];
                    max = closures[l];
                    minx = closures[l].fields.x;
                    maxx = closures[l].fields.x;
                    miny = closures[l].fields.y;
                    maxy = closures[l].fields.y;
                } else {
                    if (maxx < closures[l].fields.x){
                        maxx = closures[l].fields.x;
                    } else if (minx > closures[l].fields.x){
                        minx = closures[l].fields.x;
                    } 
                    if (maxy < closures[l].fields.y){
                        maxy = closures[l].fields.y;
                    } else if (miny > closures[l].fields.y){
                        miny = closures[l].fields.y;
                    }
                }
                
            }
            */

            // FOR POLYLINE REPRESENTATION OF CONSTRUCTION

            var list = [];
            var sublist = [];

            if (closures.length < 1){
                return;
            }
            var clen = closures.length;
            for (var i = 0; i < clen; i++){
                var ll = new google.maps.LatLng(closures[i].fields.x, closures[i].fields.y);
                sublist.push(ll);
                if (closures[i+1] == null || closures[i+1].fields.construction != closures[i].fields.construction){
                    list.push(sublist);
                    sublist = [];
                }
            }
            var llen = list.length;
            for (var i = 0; i < llen; i++){
                var zone = new google.maps.Polyline({
                path: list[i],
                geodesic: true,
                strokeColor: '#FF0000',
                strokeOpacity: 1.0,
                strokeWeight: 8
                });

                zone.setMap(map);
                closurelines.push(zone);
            }
        },
        
        // Given a list of spots and their ratings,
        // attaches a marker to the spot and pushes it to it's array.
        plotSpots: function(spots, ratings) {
            var regChecked = $("#reg_check").is(':checked');
            var handiChecked = $("#handi_check").is(':checked');
            var motoChecked = $("#moto_check").is(':checked');
            var spotsLength = spots.length;
            for (var i = 0; i < spotsLength; i++) {
                var spot = spots[i].fields;
                var rating = ratings[Number(spot.name)];
                var latlng = new google.maps.LatLng(spot.lat , spot.lng);
                var type = spot.type;
                var imgurl;
                var whatMap;              
                if (type==regStr && regChecked ||
                    type==handiStr && handiChecked ||
                    type==motoStr && motoChecked)
                    whatMap = map;
                else whatMap = null;
                
                if (type==regStr &&
                    !self.isAcceptablePrice(parseFloat(spot.rate.split("$")[1])))
                    whatMap = null;
                
                if (type==regStr &&
                    !self.isAcceptableTime(spot.timeOfEffect))
                    whatMap = null;

                imgurl = self.chooseIcon(spot.name, spot.type);

                var marker = new google.maps.Marker({
                                                    position: latlng,
                                                    map: whatMap,
                                                    icon: imgurl
                                                    });
                if (spot.rate) marker.setTitle(spot.rate + "*" + spot.timeOfEffect);
                if (spot.type == regStr) {
                    markers.push(marker);
                } else if (spot.type == handiStr) {
                    handimarkers.push(marker);
                } else {
                    motomarkers.push(marker);
                }
                self.attachWindowMessage(marker, spot, rating);
            }
        },

        // Takes meter data, creates a new Favorite meter, and pushes it to the array.
        pushFavMeter: function(meter) {
            var whatMap;
            if ($("#fav_check").is(':checked')) {
                whatMap = map;
            } else whatMap = null;
            var marker = new google.maps.Marker({
                                                position: new google.maps.LatLng(meter.fields.lat , meter.fields.lng),
                                                map: whatMap,
                                                icon: "static/images/favmeter.png"
                                                });
            self.attachWindowMessage(marker, meter.fields);
            favMeters.push(marker);
        },
        
        // Given a marker and it's name, type, and a reference to it's favorite button,
        // uses HTTP GET to remove the marker from the favorite spots list.
        removeFavMeter: function(marker, name, type, favButton) {
            $.get('remove_fav_meter', {meter_name: name, meter_type: type}, function(result){
                  if (result == "False") alert('It seems it was already unfavourited!');
                  // http://stackoverflow.com/questions/5767325/remove-specific-element-from-an-array
                  var index = favMeters.indexOf(marker);
                  if (index > -1) {
                  favMeters.splice(index, 1);
                  }
                  if (type == regStr) {
                  marker.setIcon("static/images/logo.png");
                  } else if (type == handiStr) {
                  marker.setIcon("static/images/handilogo.png");
                  } else {
                  marker.setIcon("static/images/motorlogo.png");
                  }
                  favButton.value = "<3";
                  });
        },

        // For every marker in marklist, sets the visibility to the given map.
        setAllMap: function(map, marklist) {
            for (var i = 0; i < marklist.length; i++) {
                marklist[i].setMap(map);
            }
        },
        
        // Given a lat/lng, sets the standard marker there
        setMarker: function(latlng) {
            if (marker) {
                self.updateMarker(latlng);
            } else {
                self.addMarker({'latlng': latlng, 'draggable': true});
            }
        },

        // Given spot data and rating,
        // returns a string to be used in a marker's personal window.
        setMarkerWindowText: function(spot, rating) {
            var title = 'Meter No. ' + spot.name;
            var rate = spot.rate ? spot.rate : "";
            var time = spot.timeOfEffect ? spot.timeOfEffect + '<br>': "";
            var timeLimit = spot.timeLimit ? spot.timeLimit + '<br>': "";
            var ratingStr = 'Rating: ' + ((rating == 0)? "No ratings yet" : rating);
            if (spot.type == regStr) {
                title = '<a href="/regular/meter/' + spot.name + '/"' + '<b>Regular - </b>' + title + '</a>';
            } else if (spot.type == handiStr) {
                title = '<a href="/handicap/meter/' + spot.name + '/"' + '<b>Handicap - </b>' + title + '</a>';
            } else if (spot.type == motoStr) {
                title = '<a href="/motorcycle/meter/' + spot.name + '/"' + '<b>Motorcycle - </b>' + title + '</a>';
            }
            return title + "   " + rate + '<br>' + time + timeLimit + ratingStr + '<br>';
        },

        // For all markers in marklist, show them all on the map
        showType: function(marklist) {
            self.setAllMap(map, marklist);
        },
        
        // Unplots all the markers and clears the marker lists.
        unplotAll: function() {
            self.hideType(markers);
            markers = [];
            
            self.hideType(handimarkers);
            handimarkers = [];
            
            self.hideType(motomarkers);
            motomarkers = [];

            self.unplotLine(closurelines);
            closurelines = [];
        },
        
        // Given closure lines, unplots them.
        unplotLine: function(lines) {
            for (var i = 0; i < lines.length; i++){
                lines[i].setMap(null);
            }
        },

        // Given a lat/lng, puts the marker there
        updateMarker: function(latlng) {
            marker.setPosition(latlng);
        }
    }

    return self;
}

$(document).ready(function() {
    var googlemap = googleMapAdmin();
    googlemap.initialize();
});