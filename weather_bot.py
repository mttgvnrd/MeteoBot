import requests
from datetime import datetime

def get_forecast(city_name, api_key):
    """Ottiene previsioni a 5 giorni con dati ogni 3 ore"""
    base_url = "http://api.openweathermap.org/data/2.5/forecast"
    
    try:
        response = requests.get(
            base_url,
            params={
                'q': city_name,
                'appid': api_key,
                'units': 'metric',
                'lang': 'it'
            },
            timeout=5
        )
        response.raise_for_status()
        
        data = response.json()
        
        # Estrae solo i dati rilevanti (1 previsione al giorno)
        daily_forecasts = []
        for item in data['list']:
            if item['dt_txt'].endswith("12:00:00"):  # Prendi solo le previsioni di mezzogiorno
                daily_forecasts.append({
                    'date': item['dt_txt'].split()[0],
                    'temp': item['main']['temp'],
                    'description': item['weather'][0]['description'].capitalize(),
                    'icon': item['weather'][0]['icon']
                })
        
        return daily_forecasts[:5]  # Limita a 5 giorni
        
    except Exception as e:
        return {'error': str(e)}

def get_weather(city_name, api_key):
    """Ottiene i dati meteo da OpenWeatherMap"""
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    
    try:
        response = requests.get(
            base_url,
            params={
                'q': city_name,
                'appid': api_key,
                'units': 'metric',
                'lang': 'it'
            },
            timeout=5
        )
        response.raise_for_status() 
        
        data = response.json()
        
        return {
            'city': data.get('name', city_name),
            'temp': data['main']['temp'],
            'description': data['weather'][0]['description'].capitalize(),
            'icon': data['weather'][0]['icon'],
            'details': {
                'Percepito': f"{data['main']['feels_like']}°C",
                'Umidità': f"{data['main']['humidity']}%",
                'Vento': f"{data['wind']['speed']} km/h"
            },
            'timestamp': datetime.now().strftime('%H:%M | %d/%m')
        }
        
    except Exception as e:
        return {'error': str(e)}
    except requests.exceptions.RequestException as e:
        return {'error': f"Errore di rete: {str(e)}"}
    except ValueError as e:
        return {'error': "Dati API non validi"}
        