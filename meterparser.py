import os
import xml.etree.ElementTree as ET
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'parkwhale.settings')

#db superuser - username: parkwhale, email: pw@pw.com, password: pw

import django
django.setup()

from pw.models import Meter, HandicappedMeter, MotorcycleMeter

### METER TYPES ###

class RMeter:
    ''' a set of x,y coordinates '''

    def __init__(self):
        self.name = 0
        self.lng = -1
        self.lat = -1
        self.timeOfEffect = "ERROR"
        self.timeLimit = ""
        self.rate = ""
        self.type = "regular"

class HMeter:
    ''' locations of handicapped parking'''

    def __init__(self):
        self.name = 0
        self.lng = -1
        self.lat = -1
        self.type = "handicap"

class MMeter:
    '''locations of motorcycle parking'''

    def __init__(self):
        self.name = 0
        self.lng = -1
        self.lat = -1
        self.type = "motorcycle"

### PARSER CLASSES ###

class RegularParser:
    def __init__(self, string):
        self.tree = ET.parse(string)

    def parse(self):
        acc = 0;
        list_of_coordinates = []
        for elem in self.tree.iter():
            if elem.tag == '{http://www.opengis.net/kml/2.2}Placemark':
                m = RMeter()
                for child in elem.iter():
                    if child.tag == "{http://www.opengis.net/kml/2.2}description":
                        work = child.text
                        try:
                            m.timeOfEffect = self.extract(work, "METER IN EFFECT")
                            m.timeLimit = self.extract(work, "Time Limit")
                            m.rate = self.extract(work, "Rate")
                        except ValueError:
                            pass
                    if child.tag == "{http://www.opengis.net/kml/2.2}coordinates":
                        coords = child.text.split(',')
                        m.lng = float(coords[0])
                        m.lat = float(coords[1])
                if (m.timeOfEffect != "ERROR"):
                    m.name = acc
                    acc += 1
                    list_of_coordinates.append(m)
        return list_of_coordinates


    def extract(self, mainstring, substring):
        start = mainstring.index(substring)
        fin = start
        while mainstring[fin] != "<":
            fin += 1
        return mainstring[start:fin]

class MotorcycleParser:
    def __init__ (self, string):
        self.tree = ET.parse(string)

    def parse(self):
        acc = 0
        list_of_coordinates = []
        for elem in self.tree.iter():
            if elem.tag == '{http://www.opengis.net/kml/2.2}Placemark':
                m = MMeter()
                for child in elem.iter():
                    if child.tag == "{http://www.opengis.net/kml/2.2}coordinates":
                        coords = child.text.split(',')
                        m.lng = float(coords[0])
                        m.lat = float(coords[1])
                m.name = acc
                acc += 1
                list_of_coordinates.append(m)
        return list_of_coordinates

class HandicappedParser:
    def __init__ (self, string):
        self.tree = ET.parse(string)

    def parse(self):
        acc = 0
        list_of_coordinates = []
        for elem in self.tree.iter():
            if elem.tag == '{http://www.opengis.net/kml/2.2}Placemark':
                m = HMeter()
                for child in elem.iter():
                    if child.tag == "{http://www.opengis.net/kml/2.2}coordinates":
                        coords = child.text.split(',')
                        m.lng = float(coords[0])
                        m.lat = float(coords[1])
                m.name = acc
                acc += 1
                list_of_coordinates.append(m)
        return list_of_coordinates

### FUNCTIONS TO POPULATE THE DATABASE ###

def add_meter(meter):
    m = Meter.objects.get_or_create(name=meter.name, lat=meter.lat, lng=meter.lng, timeOfEffect=meter.timeOfEffect, timeLimit=meter.timeLimit, rate=meter.rate, type=meter.type)[0]
    m.save()
    return m

def add_handi_meter(meter):
    m = HandicappedMeter.objects.get_or_create(name=meter.name, lat=meter.lat, lng=meter.lng, type=meter.type)[0]
    m.save()
    return m

def add_moto_meter(meter):
    m = MotorcycleMeter.objects.get_or_create(name=meter.name, lat=meter.lat, lng=meter.lng, type=meter.type)[0]
    m.save()
    return m

def populate():
    print "Initializing regular meter parser..."

    r = RegularParser('meters.kml')
    list_of_regular_meters = r.parse()

    print "Regular meters parsed..."

    for l in list_of_regular_meters:
        add_meter(l)

    print "Regular meters added to database, initializing motorcycle meter parser"

    m = MotorcycleParser('motorcycle_parking.kml')
    list_of_motorcycle_meters = m.parse()

    print "Motorcycle meters parsed..."

    for l in list_of_motorcycle_meters:
        add_moto_meter(l)

    print "Motorcycle meters added to database, initializing motorcycle meter parser"

    h = HandicappedParser('disability_parking.kml')
    list_of_handicapped_meters = h.parse()

    print "Handicapped meters parsed..."

    for l in list_of_handicapped_meters:
        add_handi_meter(l)

    print "Handicapped meters added to database, printing outputs..."

    for x in Meter.objects.all():
        print "- {0}".format(str(x.name))

    for x in MotorcycleMeter.objects.all():
        print "- {0}".format(str(x.name))

    for x in HandicappedMeter.objects.all():
        print "- {0}".format(str(x.name))

    print "Running test suite..."

    print "Running regular meter tests..."

    regtest = True

    for x in list_of_regular_meters:
        if x.timeOfEffect == "ERROR" or x.timeLimit == "" or x.rate == "":
            return x.name, " has failed, strings are not filled..."
            regtest = False
        if x.lat == -1 or x.lng == -1 :
            return x.name, " has failed, lat/long is incorrect..."
            regtest = False
    
    if len(list_of_regular_meters) != 9849:
        print "Regular meters list size is incorrect"
        regtest = False
        test = 0
        for x in list_of_regular_meters:
            if x.name != test:
                print x.name, " is incorrect"
                test = x.name + 1
            else:
                test = test + 1

    if regtest:
        print "All tests have passed, beginning motorcycle tests..."
    else:
        print "Some tests have failed, check output..."

    mototest = True

    for x in list_of_motorcycle_meters:
        if x.lat == -1 or x.lng == -1 :
            return x.name, " has failed, lat/long is incorrect..."
            mototest = False

    if len(list_of_motorcycle_meters) != 242:
        print "Motorcycle meters list size is incorrect"
        mototest = False
        test = 0
        for x in list_of_motorcycle_meters:
            if x.name != test:
                print x.name, " is incorrect"
                test = x.name + 1
            else:
                test = test + 1

    if mototest:
        print "All tests have passed, beginning handicapped tests..."
    else:
        print "Some tests have failed, check output..."

    handitest = True

    for x in list_of_handicapped_meters:
        if x.lat == -1 or x.lng == -1 :
            return x.name, " has failed, lat/long is incorrect..."
            handitest = False

    if len(list_of_motorcycle_meters) != 242:
        print "Motorcycle meters list size is incorrect"
        handitest = False
        test = 0
        for x in list_of_handicapped_meters:
            if x.name != test:
                print x.name, " is incorrect"
                test = x.name + 1
            else:
                test = test + 1

    if handitest:
        print "All tests have passed, beginning handicapped tests..."
    else:
        print "Some tests have failed, check output..."

    if handitest and mototest and regtest:
        print "All tests passed, all classes operating properly."
    else:
        print "Some tests failed, review code..."

### RUN ###

if __name__ == '__main__':
    print "Starting ParkWhale population script..."
    populate()





