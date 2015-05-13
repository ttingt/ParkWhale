from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from models import MotorcycleMeter, HandicappedMeter, Meter
from django.contrib.auth.models import User

class seleniumRatingTest(StaticLiveServerTestCase):
    def test_rating(self):
        typeAll = "handicap"
        name1 = 1234
        lat1 = 49.280999
        lng1 = -123.120371
        handiMeter1 = HandicappedMeter.objects.create(name=name1, lat=lat1, lng=lng1, type=typeAll)
        driver = webdriver.Firefox()
        driver.get(self.live_server_url)
        driver.find_element_by_css_selector("a[href*='register']").click()
        registration_name = driver.find_element_by_id("id_username")
        registration_email = driver.find_element_by_id("id_email")
        registration_password = driver.find_element_by_id("id_password")
        registration_name.send_keys("user")
        registration_email.send_keys("user@example.com")
        registration_password.send_keys("1234")
        driver.find_element_by_name("submit").click()
        driver.get(self.live_server_url)
        driver.find_element_by_css_selector("a[href*='login']").click()
        admin_name = driver.find_element_by_name('username')
        admin_name.send_keys("user")
        admin_name = driver.find_element_by_name('password')
        admin_name.send_keys("1234")
        driver.find_element_by_class_name('pwbutton').click()
        driver.get((
        '%s%s' % (self.live_server_url, "/handicap/meter/1234")
        ))
        driver.find_element_by_=id('rate1').click()
        #check admin site
        
class seleniumTestRegisterForParkwhale(StaticLiveServerTestCase):
    def test_register_for_parkwhale(self):
        User.objects.create_superuser(
            username='admin',
            password='admin',
            email='admin@example.com'
        )
          
        driver = webdriver.Firefox()
        driver.get((
        '%s%s' % (self.live_server_url, "/admin/")
        ))
        driver.implicitly_wait(5)
        admin_name = driver.find_element_by_id('id_username')
        admin_name.send_keys("admin")
        admin_password = driver.find_element_by_id('id_password')
        admin_password.send_keys("admin")
        admin_name.submit()
        driver.find_element_by_css_selector("a[href*='/admin/pw/userprofile/']").click()
        self.assertEqual(driver.find_element_by_class_name('paginator').text[0], '0')
          
        #register on site
        driver.get(self.live_server_url)
        driver.find_element_by_css_selector("a[href*='logout']").click()
        driver.get(self.live_server_url)
        driver.find_element_by_css_selector("a[href*='register']").click()
        registration_name = driver.find_element_by_id("id_username")
        registration_email = driver.find_element_by_id("id_email")
        registration_password = driver.find_element_by_id("id_password")
        registration_name.send_keys("user")
        registration_email.send_keys("user@example.com")
        registration_password.send_keys("1234")
        driver.find_element_by_name("submit").click()
          
        #see if registration worked
        driver.get((
             '%s%s' % (self.live_server_url, "/admin/")
         ))
        driver.implicitly_wait(5)
        admin_name = driver.find_element_by_id('id_username')
        admin_name.send_keys("admin")
        admin_password = driver.find_element_by_id('id_password')
        admin_password.send_keys("admin")
        admin_name.submit()
        driver.find_element_by_css_selector("a[href*='/admin/pw/userprofile/']").click()
        self.assertEqual(driver.find_element_by_class_name('paginator').text[0], '1')
        driver.quit()
         
          
          
class seleniumTestMeterIconOnClick(StaticLiveServerTestCase):
    def test_meter_icon_on_click(self):
        User.objects.create_superuser(
            username='admin',
            password='admin',
            email='admin@example.com'
        )
           
        driver = webdriver.Firefox()
        driver.get(self.live_server_url)
           
        typeAll = "handicap"
        name1 = 1234
        lat1 = 49.280999
        lng1 = -123.120371
        handiMeter1 = HandicappedMeter.objects.create(name=name1, lat=lat1, lng=lng1, type=typeAll)
        handiMeter1.save()
        search_box = driver.find_element_by_id("id_address")
        search_box.send_keys( "robson and granville")
        search_box.send_keys(Keys.RETURN)
        driver.implicitly_wait(10)
        driver.quit()
          
class seleniumTestRegister(StaticLiveServerTestCase):
       
    def test_create_super_user(self):
           
        #create the super user
        User.objects.create_superuser(
            username='admin',
            password='admin',
            email='admin@example.com'
        )
           
        #start environment
        driver = webdriver.Firefox()
        driver.get(self.live_server_url)
           
        #check login works with correct values
        driver.get((
             '%s%s' % (self.live_server_url, "/admin/")
         ))
        driver.implicitly_wait(5)
        admin_name = driver.find_element_by_id('id_username')
        admin_name.send_keys("admin")
        admin_password = driver.find_element_by_id('id_password')
        admin_password.send_keys("admin")
        admin_name.submit()
           
        #check super user is in database
        driver.find_element_by_css_selector("a[href*='/admin/auth/user/']").click()
        driver.implicitly_wait(3)
        self.assertEqual(driver.find_element_by_class_name('paginator').text[0], '1')
        driver.quit()
     
     
class MotorcycleMeterTestCase(StaticLiveServerTestCase):
    def test_create_motorcycle_meters(self):
        User.objects.create_superuser(
            username='admin',
            password='admin',
            email='admin@example.com'
        )
          
        #assert that meterobject is not already there
        driver = webdriver.Firefox()
        driver.get((
        '%s%s' % (self.live_server_url, "/admin/")
        ))
        driver.implicitly_wait(5)
        admin_name = driver.find_element_by_id('id_username')
        admin_name.send_keys("admin")
        admin_password = driver.find_element_by_id('id_password')
        admin_password.send_keys("admin")
        admin_name.submit()
        driver.find_element_by_css_selector("a[href*='/admin/pw/motorcyclemeter/']").click()
        self.assertEqual(driver.find_element_by_class_name('paginator').text[0], '0')
          
        mm1 = MotorcycleMeter.objects.create(name= 0000, lat=123.2265, lng=49.223, type="blue")
        mm2 = MotorcycleMeter.objects.create(name= 1111, lat=123.2278, lng=49.225, type="blue")
  
        self.assertEqual(mm1.name, 0000)
        self.assertEqual(mm2.name, 1111)
  
        self.assertEqual(mm1.lat, 123.2265)
        self.assertEqual(mm2.lat, 123.2278)
  
        self.assertEqual(mm1.lng, 49.223)
        self.assertEqual(mm2.lng, 49.225)
  
        self.assertEqual(mm1.type, "blue")
        self.assertEqual(mm2.type, "blue")
          
        driver.get((
        '%s%s' % (self.live_server_url, "/admin/")
        ))
        driver.implicitly_wait(5)
        driver.find_element_by_css_selector("a[href*='/admin/pw/motorcyclemeter/']").click()
        self.assertEqual(driver.find_element_by_class_name('paginator').text[0], '2')
        driver.quit()
          
  
class MeterMethodTests(StaticLiveServerTestCase):
    def testCreateRegularMeter(self):
        #create super user
        User.objects.create_superuser(
            username='admin',
            password='admin',
            email='admin@example.com'
        )
          
        #assert that meterobject is not already there
        driver = webdriver.Firefox()
        driver.get((
        '%s%s' % (self.live_server_url, "/admin/")
        ))
        driver.implicitly_wait(5)
        admin_name = driver.find_element_by_id('id_username')
        admin_name.send_keys("admin")
        admin_password = driver.find_element_by_id('id_password')
        admin_password.send_keys("admin")
        admin_name.submit()
        driver.find_element_by_css_selector("a[href*='/admin/pw/meter/']").click()
        self.assertEqual(driver.find_element_by_class_name('paginator').text[0], '0')
          
        #create meter object
        str = "12345678901234567890123456789012345678901234567890123456789012345"
        name = 666666
        lat = 0.0
        lon = 0.0
        meter = Meter.objects.create(name=name, lat=lat, lng=lon, timeOfEffect=str, timeLimit=str, rate=str, type=str)
          
        #see that the fields are correct
        self.assertEqual(meter.lng, lon)
        self.assertEqual(meter.lat, lat)
        self.assertEqual(len(meter.timeLimit), 65)
        self.assertEqual(len(meter.rate), 65)
        self.assertEqual(len(meter.type), 65)
          
        #see if what we created is now populating admin
        driver.get((
        '%s%s' % (self.live_server_url, "/admin/")
        ))
        driver.implicitly_wait(5)
        driver.find_element_by_css_selector("a[href*='/admin/pw/meter/']").click()
        self.assertEqual(driver.find_element_by_class_name('paginator').text[0], '1')
        driver.quit()
          
          
      
class HandiMeterTests(StaticLiveServerTestCase):
    def testCreateHandicappedMeter(self):
           
        #create super user
        User.objects.create_superuser(
            username='admin',
            password='admin',
            email='admin@example.com'
        )
  
        #assert that Handimeter objects are not already created
        driver = webdriver.Firefox()
        driver.get((
             '%s%s' % (self.live_server_url, "/admin/")
         ))
        driver.implicitly_wait(5)
        admin_name = driver.find_element_by_id('id_username')
        admin_name.send_keys("admin")
        admin_password = driver.find_element_by_id('id_password')
        admin_password.send_keys("admin")
        admin_name.submit()
        driver.find_element_by_css_selector("a[href*='/admin/pw/handicappedmeter/']").click()
        self.assertEqual(driver.find_element_by_class_name('paginator').text[0], '0')
  
        #create handicapped meter object
        typeAll = "1111111111222222222233333333334444444444555555555566666666667777777777"
        name1 = 1234
        name2 = 5678
        lat1 = 49.256072
        lat2 = 49249573
        lng1 = -123.114129 
        lng2 = -123.168717
        handiMeter1 = HandicappedMeter.objects.create(name=name1, lat=lat1, lng=lng1, type=typeAll)
        handiMeter2 = HandicappedMeter.objects.create(name=name2, lat=lat2, lng=lng2, type=typeAll)
           
        #see that the fields are correct
        self.assertEqual(handiMeter1.name, name1)
        self.assertEqual(handiMeter2.name, name2)
        self.assertEqual(handiMeter1.type, typeAll)
        self.assertEqual(handiMeter2.type, typeAll)
           
        #see if what we created is there
        driver.get((
             '%s%s' % (self.live_server_url, "/admin/")
         ))
        driver.implicitly_wait(5)
        driver.find_element_by_css_selector("a[href*='/admin/pw/handicappedmeter/']").click()
           
        #see if the number of objects put into admin makes sense
        self.assertEqual(driver.find_element_by_class_name('paginator').text[0], '2')
        driver.quit()
