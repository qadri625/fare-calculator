from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

def get_coordinates(city):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        'format': 'json',
        'q': city,
        'countrycodes': 'pk',
        'limit': 1
    }
    headers = {
        'User-Agent': 'FareCalculator/1.0'
    }
    response = requests.get(url, params=params, headers=headers)
    data = response.json()
    if data:
        return float(data[0]['lat']), float(data[0]['lon'])
    else:
        return None

def get_distance(lat1, lon1, lat2, lon2):
    url = f"https://router.project-osrm.org/route/v1/driving/{lon1},{lat1};{lon2},{lat2}"
    response = requests.get(url)
    data = response.json()
    if 'routes' in data and data['routes']:
        distance_m = data['routes'][0]['distance']
        return distance_m / 1000  # to km
    else:
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    from_city = request.form.get('from')
    to_city = request.form.get('to')
    
    from_coords = get_coordinates(from_city)
    to_coords = get_coordinates(to_city)
    
    if not from_coords or not to_coords:
        return jsonify({'error': 'Invalid city name(s). Please check spelling and ensure cities are in Pakistan.'})
    
    lat1, lon1 = from_coords
    lat2, lon2 = to_coords
    
    distance_km = get_distance(lat1, lon1, lat2, lon2)
    if distance_km is None:
        return jsonify({'error': 'Unable to calculate distance. Please try different cities.'})
    
    distance_rounded = round(distance_km, 1)
    fare = round(1.9 * distance_km + 220)
    
    return jsonify({
        'distance': distance_rounded,
        'fare': fare
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)