import os
import xml.etree.ElementTree as ET
import urllib2

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'parkwhale.settings')

#db superuser - username: parkwhale, email: pw@pw.com, password: pw

import django
django.setup()

from pw.models import RoadConstruction, LatLong

class RoadClosure:
	def __init__(self):
		self.num = 0
		self.route = []
		self.term = ""
		self.description = ""

class RoadClosureParser:

	def __init__(self):
		self.url = 'http://vanmapp2.vancouver.ca/georss/roadahead_georss.xml'
		self.rss = ET.parse(urllib2.urlopen(self.url))
		self.listofclosures = []

	def parse(self):
		i = 0
		for child in self.rss.iter():
			if child.tag == '{http://www.w3.org/2005/Atom}entry':
				e = RoadClosure()
				for entry in child.iter():
					e.num = i
					if entry.tag == '{http://www.w3.org/2005/Atom}content':
						e.description = entry.text
					if entry.tag == '{http://www.w3.org/2005/Atom}category':
						if str(entry.attrib) == "{'term':'In Process'}":
							e.term = "In Process"
						elif str(entry.attrib) == "{'term':'Upcoming Project'}":
							e.term = "Upcoming Project"
						else:
							e.term = "Road Closure"
					if entry.tag == '{http://www.georss.org/georss}line':
						e.route = entry.text.split()
				self.listofclosures.append(e)
				i = i + 1

		for closure in self.listofclosures:
			print closure.description
			print closure.term
			print closure.route

		return self.listofclosures



def add_closure(closure):

    m = RoadConstruction.objects.get_or_create(num=closure.num, description=closure.description, status=closure.term)[0]
    m.save()

    i = 0
    while (i < len(closure.route)):
    	a = float(closure.route[i])
    	b = float(closure.route[i+1])
    	l = LatLong.objects.get_or_create(x=a, y=b, construction=m)[0]
    	l.save()
    	i = i + 2

    return m



def populate():
    print "Initializing closure parser..."

    parser = RoadClosureParser()
    loc = parser.parse()

    print "Closures parsed..."

    for l in loc:
        add_closure(l)

    print "Closures added to database."



if __name__ == '__main__':
    print "Starting ParkWhale population script..."
    populate()

