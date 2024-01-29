from flask import Flask, render_template, request
import requests

app = Flask(__name__)

def get_weather(api_key, city):
    url = "http://api.openweathermap.org/data/2.5/weather"
    params = {'q': city, 'appid': api_key, 'units': 'metric'}

    try:
        response = requests.get(url, params=params)
        data = response.json()
        return {
            'city': city,'temperature': data['main']['temp'],'description': data['weather'][0]['description'],'humidity': data['main']['humidity'],'wind_speed': data['wind']['speed']
        }

    except requests.RequestException as e:
        return {'error': f"Error connecting to the API: {e}"}

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_info, error = None, None

    if request.method == 'POST':
        city = request.form.get('city')
        api_key = '6fbaac4bb71257547902ada6cc55d38a'

        try:
            weather_info = get_weather(api_key, city)
        except Exception as e:
            error = f"An error occurred: {e}"

    return render_template('index.html', weather_info=weather_info, error=error)

if __name__ == "__main__":
    app.run(debug=True,port=5000)
