### ParkWhale ###
An app to serve your Vancouver street parking needs.
<br>
Created by Team 1000 Whaling Corpses as an academic project for CPSC310 Winter2015.<br>
Team members: Hoi Ting (Ting Ting) Tai, Kieran Collery, Daniel Hill, and Anthony Campbell. <br>
<br>
This app was built using Django and a good deal of JavaScript focused around the Google Maps API. Our team followed the scrum process with our lab teaching assistant acting as our Scrum Master. Features were split into 2 sprints, with the submitted project completed on April 2, 2015. <br>
<br>
The deployed web app may be found at: [kcollery.pythonanywhere.com] (http://kcollery.pythonanywhere.com)

-----------------

###Summary###

This application serves the purpose of providing a simple website to determine the best place to park in Vancouver based on a destination and type of parking spot.<br>
<br>
The app will take an address in and then return in Google Maps form a series of map tags/zones showing parking spots and their prices near your destination, road closures in the area so you can avoid traffic backup, and handicap/motorcycle spots. These come from City of Vancouver databases and would be parsed on the fly and returned. The user can also login and rate good spots; this data can be aggregated and then other users can see what rating a spot has by other parkers.

-----------------

###The Scrum Process###

January to April 2015<br>
Scrum Master: Our course/lab teaching assistant <br>
Sprints: 2<br>
[User Stories] (https://drive.google.com/file/d/0B6EvdY5DFlgkck1jcFF3TkNnczA/view?usp=sharing)

-----------------

Datasets Used (from Vancouver's Open Data Catalogue):<br>
* [Parking Meter Dataset] (http://data.vancouver.ca/datacatalogue/parkingMeter.htm)
* [Road Closures Dataset] (http://data.vancouver.ca/datacatalogue/roadAhead.htm Motorcycle)
* [Parking Spots Dataset] (http://data.vancouver.ca/datacatalogue/motorcycleParking.htm Disability)
* [Parking Spots Dataset] (http://data.vancouver.ca/datacatalogue/disabilityParking.htm)
