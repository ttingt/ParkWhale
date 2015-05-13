
/*
Add/Remove Favourite Meters

How it works:

A favourite/unfavourite button will be displayed to allow the user to add or remove
that favourite.

This script expects:
    <input id="fav-button" type="button">
*/

function favAdmin() {
    var button;
    var favStr = "<3 Me";
    var notFavStr = "<\\3 Me"

    var self = {
        initialize: function() {
            button = document.getElementById("fav-button");
            if (isFav == "False") {
                button.value = favStr;
            } else {
                button.value = notFavStr;
            }
            self.attachHandlers();
        },

        attachHandlers: function() {
            button.addEventListener("click", function() {
                if (isFav == "False") {
                    self.addFavMeter(meterName, meterType);
                } else {
                    self.removeFavMeter(meterName, meterType);
                }
            });
        },

        addFavMeter: function(name, type) {
            $.get('../../../add_fav_meter/', {meter_name: name, meter_type: type}, function(result){
                if (result == "True") {
                    button.value = notFavStr;
                    isFav = "True";
                } else {
                    alert('Login to save favourite spots!');
                }
            });
        },

        removeFavMeter: function(name, type) {
            $.get('../../../remove_fav_meter', {meter_name: name, meter_type: type}, function(result){
                if (result == "False") {
                    alert('This spot has already been unfavourited.');
                }
                button.value = favStr;
                isFav = "False";
            });
        },
    }

    return self;
}

$(document).ready(function() {
    var fav = favAdmin();
    fav.initialize();
});