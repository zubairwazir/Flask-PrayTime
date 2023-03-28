from flask import Flask, render_template, request
from geopy.geocoders import Nominatim
import requests, json, time

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/prayer-time', methods=['POST'])
def prayer_time():
    address = request.form['location']
    geolocator = Nominatim(user_agent="iftar-time-app")
    location = geolocator.geocode(address)
    latitude = location.latitude
    longitude = location.longitude

    # Send a GET request to the API endpoint to get the Prayer time
    url = f"https://api.aladhan.com/v1/timings/{int(time.time())}?latitude={latitude}&longitude={longitude}&method=1&school=1"
    response = requests.get(url)
    data = json.loads(response.text)
    fajr = data['data']['timings']['Fajr']
    dhuhr = data['data']['timings']['Dhuhr']
    asr = data['data']['timings']['Asr']
    maghrib = data['data']['timings']['Maghrib']
    isha = data['data']['timings']['Isha']

    return render_template('prayer-time.html', fajr=fajr, dhuhr=dhuhr, asr=asr, maghrib=maghrib, isha=isha, city = address)

if __name__ == "__main__":
    app.run(debug=True)
