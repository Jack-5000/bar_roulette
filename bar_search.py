import os 
from dotenv import load_dotenv
from google.maps import places_v1
import googlemaps
from google.type import latlng_pb2
import sys
import asyncio

load_dotenv()
places_key = os.getenv("GOOGLE_PLACES_API")

#Parses through data received from Google maps API to single out lat and lng 
def geodata_parser(geo_data: str):
    startindex = geo_data.find("location")
    
    location_chars = geo_data[startindex]
    location_string = " "
    endindex = startindex
    while location_chars != "}":
        location_string += location_chars
        endindex = endindex + 1
        location_chars = geo_data[endindex]
    
    location_string = location_string.replace("location", "").replace("'", "").replace("{", "").replace(":", "")
    location_list = location_string.split(", ")
    location_list[0] = location_list[0].replace("lat", "").strip()
    location_list[1] = location_list[1].replace("lng", "").strip()

    return location_list

#Gets latitude and longitude from a given address. location_list[0] = latitude, location_list[1] = longitude 
def geocoder(address: str):
    geo_client = googlemaps.Client(key=str(places_key))
    geo_list = geo_client.geocode(address)

    if len(geo_list) == 0:
        return 0
    else:
       geo_data = str(geo_list[0].get('geometry'))

    return geodata_parser(geo_data)
    
def miles_to_meters(miles: int):
    if miles > 31 or miles < 0:
        return -1
    else:
        meters = miles * 1609
    
    return meters

async def bar_search(address: str, dist_miles: int):

    search_client = places_v1.PlacesAsyncClient(client_options={"api_key": str(places_key)})

    coords_list = geocoder(address)
    dist_meters = miles_to_meters(dist_miles)
    if dist_meters == -1 or coords_list == 0:
        sys.exit(1)

    lat = float(coords_list[0])
    lng = float(coords_list[1])

    center_point = latlng_pb2.LatLng(latitude=lat, longitude=lng)
    circle_area = places_v1.types.Circle(
        center=center_point,
        radius=dist_meters
    )

    location_bias = places_v1.SearchTextRequest.LocationBias(circle=circle_area)
    query = "bars with alcohol"
    
    request = places_v1.SearchTextRequest(
        text_query=query,
        location_bias=location_bias,
        included_type="bar",
        open_now=True
    )

    fieldmask = "places.formattedAddress,places.displayName,places.rating"

    response = await search_client.search_text(request=request, metadata=[("x-goog-fieldmask",fieldmask)])
    return response


if __name__ == '__main__':
    res = asyncio.run(bar_search("2827 Belmont Avenue Ardmore PA", 5))
    print(res)
    


