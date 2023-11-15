import requests
from datetime import datetime, timedelta
from geopy import geocoders

class GetWeather:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"

    @staticmethod
    def get_lat_long(city_name):
        geolocator = geocoders.Nominatim(user_agent="YourAppName")
        try:
            location = geolocator.geocode(city_name)
            if location:
                return location.latitude, location.longitude
            else:
                print(f"Error: Unable to retrieve coordinates for {city_name}")
                return None
        except Exception as e:
            print(f"Error: {e}")
            return None

    @staticmethod
    def getWeather(location, date):
        # OpenWeatherMap API URL for weather forecast
        api_url_forecast = 'https://api.openweathermap.org/data/2.5/forecast'

        # Get latitude and longitude using get_lat_long function
        coordinates = GetWeather.get_lat_long(location)
        if not coordinates:
            return None

        lat, lon = coordinates

        # Parameters for the API request
        params_forecast = {'lat': lat, 'lon': lon, 'exclude': 'minutely,hourly,alerts', 'appid': api_key, 'units': 'metric'}

        # API request 
        response_forecast = requests.get(api_url_forecast, params=params_forecast)
        
        # A dictionary to store the structured response
        if type(date) == str or date is None:
            weather_response = {
                'location': location,
                'date': date,
                'forecast': {}
            }
        else :   
            weather_response = {
                'location': location,
                'date': date.strftime('%Y-%m-%d'),
                'forecast': {}
            }

        # Continue with JSON parsing
        if response_forecast.status_code == 200:
            try:
                # Parse the JSON response
                weather_data_forecast = response_forecast.json()

                # Get the current date
                current_date = datetime.utcnow().date()
                if not date : date = "today"
                if str(date) == "tomorrow":
                    date = current_date + timedelta(days=1)
                    
                elif str(date) == "today" :
                    date = current_date
                else :
                    if type(date) == str:
                        try : date = datetime.strptime(date, '%Y-%m-%d').date()
                        except :
                            weather_response['forecast']['error'] = f"Error parsing date: {date}"
                            return weather_response
                # Calculate the number of days between the current date and the specified date
                days_difference = (date- current_date).days
            

                # Check if the specified date is within the forecast range
                if 0 <= days_difference < len(weather_data_forecast['list']):
                    # Extract the weather information for the specified date
                    forecast = weather_data_forecast['list'][days_difference]

                    # Extract relevant information from the JSON
                    #add celsius to the temperature

                    temperature_day = forecast['main']['temp'] 
                    temperature_min = forecast['main']['temp_min']
                    temperature_max = forecast['main']['temp_max']

                    # Add Celsius unit to the temperature values and store in the dictionary
                    weather_response['forecast']['temperature'] = {
                        'day': f"{temperature_day}°C",
                        'min': f"{temperature_min}°C",
                        'max': f"{temperature_max}°C"
    }
                else:
                    weather_response['forecast']['error'] = f"No forecast available for {date}."
            except ValueError as e:
                weather_response['forecast']['error'] = f"Error parsing JSON response: {e}"
        elif response_forecast.status_code == 404:
            print('Error: 404 Not Found')
        else:
            print('Error: Unable to retrieve data.')


        return weather_response