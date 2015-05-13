
/*
Meter Rating - User input allowed

How it works:

The radio buttons will be updated to reflect the current meter's rating score.
If the user is logged in, once a radio button is clicked, the current rating
is updated and displayed and the buttons are no longer clickable. If the user
is not logged in, they can view the current rating, but cannot rate themselves.

This script expects:
    <input id="rate1" type="radio">
    <input id="rate2" type="radio">
    <input id="rate3" type="radio">
    <input id="rate4" type="radio">
    <input id="rate5" type="radio">
*/

function ratingAdmin() {
    var labels = ["rate1", "rate2", "rate3", "rate4", "rate5"];
    var maxRating = 5;

    var self = {
        initialize: function() {
            self.renderRating();
            if (loggedIn) self.showPreviousRating();
            self.attachHandlers();
        },

        renderRating: function() {
            for (i=0; i < maxRating; i++) {
                if (i < Math.round(rating)) {
                    self.getInput(i).checked = true;
                } else {
                    self.getInput(i).checked = false;
                }
            }
        },

        showPreviousRating: function() {
            $.get('../../../get_user_rating/', {meter_name: meterName, meter_type: meterType}, function(data){
                if (data != 0)
                    $('#users-rating').html("You gave this spot a " + data + " out of 5.");
            });
        },

        attachHandlers: function() {
            $("#rate1").click(function() {self.updateRating(1);});
            $("#rate2").click(function() {self.updateRating(2);});
            $("#rate3").click(function() {self.updateRating(3);});
            $("#rate4").click(function() {self.updateRating(4);});
            $("#rate5").click(function() {self.updateRating(5);});
        },

        updateRating: function(r) {
            if (loggedIn) {
                $.get('/rate_meter/', {meterName: meterName, meterType: meterType, rate: r}, function(data) {
                    rating = data.newRating;
                    self.renderRating();
                    $('#rating-msg').html(data.msg);
                    $('#users-rating').html("You gave this spot a " + r + " out of 5.");
                    });
            } else {
                alert("Login to rate this spot!");
            }
        },

        getInput: function(i) {
              return document.getElementById(labels[i]);
        },
    }

    return self;
}

$(document).ready(function() {
    var rating = ratingAdmin();
    rating.initialize();
});