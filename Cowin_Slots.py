import requests
import time
from playsound import playsound
from itertools import cycle
from pynotifier import Notification
dist = [730]
date ='03-06-2021'

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}


def findAvailability():
    print('Searching for slots...')
    URL = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id={}&date={}'.format(
    dist[0], date)
    counter = 0
    result = requests.get(URL, headers=header)
    response_json = result.json()
    data = response_json["sessions"]
    for each in data:
        if((each["available_capacity_dose1"] > 0) & (each["min_age_limit"] == 18)):
            counter += 1
            print(each["name"])
            print(each["pincode"])
            print(each["vaccine"])
            print(each["available_capacity"])
            Notification(
                title='Vaccination Slot Found',
                description='Your can get vaccination at {} pincode:{} with {}.You must rush immediately as there are {} slots left'.format(each['name'],each['pincode'],each['vaccine'],each['available_capacity']),
                # On Windows .ico is required, on Linux - .png
                # icon_path='path/to/image/file/icon.png',
                duration=10,                              # Duration in seconds
                urgency='normal'
            ).send()
            playsound('ding-sound.mp3')
            return True
    if(counter == 0):
        playsound('Love-life.mp3')
        Notification(
                title='Vaccination Slot Found',
                description='Your can get vaccination at '+each['name']+'pincode:'+each['pincode']+'with' +
                each['vaccine']+'.You must rush as there are ' +
                each['available_capacity']+'slots left',
                # On Windows .ico is required, on Linux - .png
                # icon_path='path/to/image/file/icon.png',
                duration=5,                              # Duration in seconds
                urgency='normal'
            ).send()
        return False

# alternator = cycle((0,1))
# t = next(alternator)
while(findAvailability() != True):
    time.sleep(5)
    # t = next(alternator)
    print('Restarting the search')
    findAvailability()
