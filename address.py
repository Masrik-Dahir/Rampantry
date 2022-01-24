# import module
from geopy.geocoders import Nominatim
def find(Latitude, Longitude):
    # initialize Nominatim API
    geolocator = Nominatim(user_agent="geoapiExercises")

    location = geolocator.reverse(Latitude + "," + Longitude)

    address = location.raw['address']

    # traverse the data
    street = address.get('house_number') + " " + address.get('road')
    city = address.get('city', '')
    if (city == ""):
        city = address.get('county', '')
    state = address.get('state', '')
    zipcode = address.get('postcode')

    print('Street : ', street)
    print('City : ', city)
    print('State : ', state)
    print('Zip Code : ', zipcode)
    print(address)
    return [street, city, state, zipcode]

# Latitude = "28.6973858"
# Longitude = "-81.34892219999999"
# find(Latitude, Longitude)