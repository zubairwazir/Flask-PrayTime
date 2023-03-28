from flask import Flask, render_template, request
from geopy.geocoders import Nominatim
import requests, json, time

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/iftar-time', methods=['POST'])
def iftar_time():
    address = request.form['location']
    geolocator = Nominatim(user_agent="iftar-time-app")
    location = geolocator.geocode(address)
    latitude = location.latitude
    longitude = location.longitude

    # Send a GET request to the API endpoint to get the Iftar time
    url = f"https://api.aladhan.com/v1/timings/{int(time.time())}?latitude={latitude}&longitude={longitude}&method=1"
    response = requests.get(url)
    data = json.loads(response.text)
    iftar_time = data['data']['timings']['Maghrib']

    return render_template('iftar-time.html', iftar_time=iftar_time)

if "__main__" == "__name__":
    app.run(debug=True)