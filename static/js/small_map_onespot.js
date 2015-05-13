
/*
Displays google map with a marker placed for one given meter spot.

This script expects:
    <div id="small_map_canvas"></div>
*/

function smallMapAdmin() {
    var INITIAL_ZOOM = 18;
    var regStr = "regular";
    var handiStr = "handicap";
    var motoStr = "motorcycle";
    var favIconUrl = "../../../static/images/favmeter.png";

    var map;
    var marker;
    var latlng;
    var iconUrl;
    var button;

    var self = {
        initialize: function() {
            latlng = new google.maps.LatLng(meterLat,meterLng);
            var myOptions = {
              zoom: INITIAL_ZOOM,
              center: latlng,
              mapTypeId: google.maps.MapTypeId.SATELLITE
            };
            map = new google.maps.Map(document.getElementById("small_map_canvas"), myOptions);

            iconUrl = self.chooseIcon();
            marker = new google.maps.Marker({
                position: latlng,
                map: map,
                icon: iconUrl
            });
            if (isFav == "True") marker.setIcon(favIconUrl);

            button = document.getElementById("fav-button");
            if (loggedIn) self.attachHandlers();
        },

        chooseIcon: function() {
            var url;
            if (meterType == handiStr) {
                url = "../../../static/images/handilogo.png"
            } else if (meterType == regStr) {
                url = "../../../static/images/logo.png";
            } else {
                url = "../../../static/images/motologo.png";
            }
            return url;
        },

        updateIconIfFav: function() {
            if (isFav == "False") {
                marker.setIcon(favIconUrl);
            } else {
                marker.setIcon(iconUrl);
            }
        },

        attachHandlers: function() {
            button.addEventListener("click", function() {
                self.updateIconIfFav();
            });
        },
    }

    return self;
}

$(document).ready(function() {
    var sma = smallMapAdmin();
    sma.initialize();
});