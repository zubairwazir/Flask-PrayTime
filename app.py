from flask import Flask, render_template, request
from geopy.geocoders import Nominatim
from datetime import datetime
import requests, json, time

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/prayer-time', methods=['POST'])
def prayer_time():
    location = request.form['location']
    geolocator = Nominatim(user_agent="prayer-time-app")
    location = geolocator.geocode(location)
    latitude = location.latitude
    longitude = location.longitude

    # Send a GET request to the API endpoint to get the Prayer time
    url = f"https://api.aladhan.com/v1/timings/{int(time.time())}?latitude={latitude}&longitude={longitude}&method=1&school=1"
    response = requests.get(url)
    data = json.loads(response.text)
    timings = data['data']['timings']
    #
    date=datetime.today().date()

    # Convert the timings to AM/PM format
    prayer_times = {}
    for key in timings:
        time_obj = datetime.strptime(timings[key], '%H:%M')
        time_str = time_obj.strftime('%I:%M %p')
        prayer_times[key] = time_str

    return render_template('prayer-time.html', prayer_times=prayer_times, city=location, date=date)

if __name__ == "__main__":
    app.run(debug=True)
