# import module
from geopy.geocoders import Nominatim


def find(Latitude, Longitude):
    # initialize Nominatim API
    geolocator = Nominatim(user_agent="geoapiExercises")

    location = geolocator.reverse(Latitude + "," + Longitude)

    address = location.raw['address']

    # traverse the data
    street = address.get('house_number','') + " " + address.get('road','')
    city = address.get('county','')
    if city == "":
        city = address.get('suburb', '')
    if city == "":
        city = address.get('neighbourhood', '')
    if city == "":
        city = address.get('city', '')

    state = address.get('state', '')
    zipcode = address.get('postcode', '')

    # print('Street : ', street)
    # print('City : ', city)
    # print('State : ', state)
    # print('Zip Code : ', zipcode)
    # print(address)
    return street, city, state, zipcode

# Latitude = "47.3404659"
# Longitude = "122.7429631"
# find(Latitude, Longitude)
