from flask import Flask, render_template, request
import requests

app = Flask(__name__, template_folder='templates')

def get_weather(city, api_key):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    response = requests.get(url)
    data = response.json()
    return data

def clothing_suggestions(weather):
    if 'main' not in weather or 'weather' not in weather:
        return 'Unable to fetch weather data. Please try again later.'

    temperature = weather['main']['temp']
    humidity = weather['main']['humidity']
    wind_speed = weather['wind']['speed']
    weather_condition = weather['weather'][0]['main'].lower()

    if 'rain' in weather_condition:
        return 'Don\'t forget your umbrella and wear waterproof clothing.', 'rainy'
    elif 'cloud' in weather_condition:
        return 'It might be cloudy. Bring a light jacket just in case.', 'cloudy'
    elif temperature > 25:
        return 'It\'s hot! Wear light-colored clothing and sunscreen.', 'sunny'
    elif 15 <= temperature <= 25:
        return 'It\'s mild. A t-shirt with jeans should be fine.', 'sunny'
    else:
        return 'It\'s cold outside. Don\'t forget to bundle up.', 'cold'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        city = request.form['city']
        api_key = 'API_KEY'  # Replace with your API key
        weather_data = get_weather(city, api_key)
        suggestions, weather_type = clothing_suggestions(weather_data)
        return render_template('index.html', city=city, suggestions=suggestions, weather_type=weather_type, 
                               temperature=weather_data['main']['temp'], humidity=weather_data['main']['humidity'], 
                               wind_speed=weather_data['wind']['speed'])
    else:
        return render_template('index.html', city='', suggestions='')

if __name__ == '__main__':
    app.run(debug=True)
