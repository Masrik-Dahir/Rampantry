# import module
from geopy.geocoders import Nominatim


def find(Latitude, Longitude):
    road_types = [
        "Alley",
        "Street",
        "Avenue",
        "B road",
        "Brick Road",
        "Boulevard",
        "Bundesstraße",
        "Byway",
        "Causeway",
        "Circle",
        "Collector",
        "road",
        "Corniche",
        "Close",
        "Crescent",
        "Court",
        "Cul-de-sac",
        "Dead end",
        "Drive",
        "Frontage road",
        "Gemeindestraße",
        "Highway",
        "Kreisstraße",
        "Lane",
        "Landesstraße",
        "Living",
        "street",
        "Loop",
        "One-way street",
        "Path",
        "Place",
        "Plaza",
        "Road",
        "Roundabout",
        "Route",
        "Side road",
        "Single carriageway",
        "Stravenue",
        "Terrace",
        "Way",
        "Tree tunnel",
        "Woonerf",
        "Agricultural road",
        "Backroad",
        "Dirt road",
        "Forest road",
        "Gravel road",
        "Green lane",
        "Historic roads",
        "Trail",
        "Ice road",
        "Roman roads",
        "Sunken lane",
        "2 + 1 road",
        "2 + 2 road",
        "Arterial road",
        "Autostrasse",
        "Dual carriageway",
        "Expressway",
        "Local-express lanes",
        "Farm to Market Road",
        "Parkway",
        "Beltway",
        "Reversible lane",
        "Trunk road",
        "Turnpike",
        "Autobahn",
        "Auto-estrada",
        "Autopista",
        "Autostrada",
        "Controlled-access highway",
        "Freeway",
        "High-quality dual carriageway",
        "HQDC",
        "Interstate",
        "Highway",
        "Limited-access highway",
        "Motorway",
        "Super two",
        "Driveway",
        "Gated community",
        "Military road",
        "Private highway",
        "Private road",
        "Connector",
        "Interchange",
        "Intersection",
        "Level junction",
        "Level crossing",
        "Road diet",
        "Roundabout",
        "Concrete roads",
        "Asphalt roads",
        "Gravel roads",
        "Earthen roads",
        "Murrum roads",
        "Kankar roads",
        "Bituminous roads",
        "Bascule bridge",
        "Bus lane",
        "Canal",
        "Carpool lane",
        "Cycle track",
        "Cycling infrastructure",
        "Flight deck",
        "Footpath",
        "Pedestrian way",
        "Walking trail",
        "Nature trail",
        "Free-market roads",
        "National roads",
        "Indian route",
        "Paper street",
        "Race track",
        "Runway",
        "Stroad",
        "Shunpike",
        "Wildlife crossing"]

    # initialize Nominatim API
    try:
        Latitude = str(round(float(Latitude), 6))
        Longitude = str(round(float(Longitude), 6))
        geolocator = Nominatim(user_agent="geoapiExercises")

        location = geolocator.reverse(Latitude + "," + Longitude)

        address = location.raw['address']

        # traverse the data
        number = address.get('house_number','')
        street = address.get('road','')


        typ = street.split(" ")
        typ_ = ''
        for i in range (0, len(typ)):
            if typ[i] in road_types:
                street = street.replace(typ[i], '')
                typ_ = typ[i]

        city = address.get('county','')
        if city == "":
            city = address.get('suburb', '')
        if city == "":
            city = address.get('neighbourhood', '')
        if city == "":
            city = address.get('city', '')

        state = address.get('state', '')
        zipcode = address.get('postcode', '')
    except:
        number, street, typ_, city, state, zipcode = "", "", "", "", "", ""

    return number, street, typ_, city, state, zipcode

# Latitude = "39.567318"
# Longitude = "-78.979223"
# print(find(Latitude, Longitude))
