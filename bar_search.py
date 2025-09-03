import os 
from dotenv import load_dotenv
from google.maps import places_v1


load_dotenv()
places_key = os.getenv("GOOGLE_PLACES_API")

def geocoder(address: str):
    print("Get long and lat")

def bar_search(longitude: int, latitude: int, distance: int):

    search_client = places_v1.PlacesAsyncClient(client_options={"api_key": str(places_key)})



if __name__ == '__main__':
    print("hello")