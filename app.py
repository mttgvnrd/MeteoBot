from flask import Flask, request, jsonify, render_template
from weather_bot import get_weather, get_forecast
import os
from dotenv import load_dotenv 

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv('OWM_API_KEY')
DEBUG_MODE = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'


@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, max-age=0'
    return response

@app.route('/get_forecast', methods=['POST'])
def forecast_api():
    city = request.json.get('city')
    if not city:
        return jsonify({'error': 'Specifica una città'}), 400
    
    forecast_data = get_forecast(city, API_KEY)
    return jsonify(forecast_data)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_weather', methods=['POST'])
def weather_api():
    city = request.json.get('city')
    if not city:
        return jsonify({'error': 'Specifica una città'}), 400
    
    weather_data = get_weather(city, API_KEY)
    return jsonify(weather_data)

if __name__ == '__main__':
    app.run(debug=True)