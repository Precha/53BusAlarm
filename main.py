import googlemaps
import datetime
import os

# You need to get a Google Maps API key from https://console.developers.google.com/
# Enable the Directions API
API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')  # Set this environment variable

if not API_KEY:
    print("Please set the GOOGLE_MAPS_API_KEY environment variable.")
    exit(1)

gmaps = googlemaps.Client(key=API_KEY)

def get_next_metro_time():
    # Define the origin and destination
    origin = "Weesperplein, Amsterdam"
    destination = "Diemen Zuid, Amsterdam"
    mode = "transit"
    transit_mode = "subway"  # For metro

    # Get directions
    directions_result = gmaps.directions(origin, destination, mode=mode, transit_mode=transit_mode, departure_time=datetime.datetime.now())

    if directions_result:
        # Parse the first route
        route = directions_result[0]
        legs = route['legs'][0]
        steps = legs['steps']

        for step in steps:
            if step['travel_mode'] == 'TRANSIT':
                transit_details = step['transit_details']
                line = transit_details['line']
                if '53' in line['short_name']:
                    departure_time = transit_details['departure_time']['value']
                    dep_dt = datetime.datetime.fromtimestamp(departure_time)
                    now = datetime.datetime.now()
                    minutes = int((dep_dt - now).total_seconds() / 60)
                    if minutes >= 0:
                        return minutes

    return None

if __name__ == "__main__":
    minutes = get_next_metro_time()
    if minutes is not None:
        print(f"下一班53號捷運往Diemen Zuid將在{minutes}分鐘後到站。")
    else:
        print("無法獲取下一班車時間。")