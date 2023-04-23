###################################################################################################################################################################
# CT30A3401 Distributed Systems
# Author: Markus Taulu
# Date: 22.04.2023
# Sources: https://openweathermap.org/current (weather API), https://openweathermap.org/api/air-pollution (Air pollution API), 
# https://openweathermap.org/api/geocoding-api (Geocoding API), https://docs.python.org/3/library/xmlrpc.server.html#module-xmlrpc.server (Basic structure)
#
# Note: I have installed requests libary using an virtual environment
# microservice_3.py (Weather service)
###################################################################################################################################################################

from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import requests

## API key from OpenWeatherMap free tier
api_key = 'see moodle comment'

## Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

## Create server
with SimpleXMLRPCServer(('localhost', 8002),
                        requestHandler=RequestHandler) as server:
    server.register_introspection_functions()

    ## Weather function searches for the current weather and description of said weather from user input city
    def weather_function(location):
        ## Build the API endpoint URL
        url = f'http://api.openweathermap.org/data/2.5/weather?q={location},FI&appid={api_key}&units=metric'
        
        try:
            ## Send a GET request to the API endpoint URL and store the response
            response = requests.get(url)

            ## Extract the JSON data from the response
            data = response.json()
            ## save the current weather information for searched city
            results = f"Current temperature in {location} is {data['main']['temp']}°C\nCurrent weather description: {data['weather'][0]['description']}"
        
        ## Error handling
        except requests.exceptions.HTTPError:
            results = "An http error occurred"
        except Exception:
            results = "An error occurred"
        
        ## Return the string
        return results
    server.register_function(weather_function, 'weather')

    ## Air pollution function searches for the current pollution and CO from user inputted city
    def airpollution_function(location):
        ## AQI levels response from API is [1, 2, 3, 4, 5]
        aqi_levels = ["Good", "Fair", "Moderate", "Poor", "Very Poor"]
        
        ## Build the API endpoint URL
        geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={location}&limit=1&appid={api_key}"
        try:
            ## Get the geographical coordinates for the city using Geocoding API
            response = requests.get(geo_url)
            data = response.json()
            latitude = data[0]["lat"]
            longitude = data[0]['lon']

        except Exception:
            results = "Error occurred while getting geographical coordinates"
            return results

        ## Get the air pollution level using OpenWeatherMap API, using the lat & lon from Geocoding API
        pollution_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={latitude}&lon={longitude}&appid={api_key}"
        try:
            ## Get the air pollution and CO levels for the city using Air pollution API
            response = requests.get(pollution_url)
            data = response.json()
            ## As the response is 1-5 we remove 1 to get the correct index
            aqi = int(data['list'][0]['main']['aqi']) - 1
            ## Save the string as result
            results = f"The air pollution level in {location} is {aqi_levels[aqi]} and the amount of CO is {data['list'][0]['components']['co']}"
        
        ## Generic Error handling
        except Exception:
            results = "Error occurred while getting air pollution data"
        
        ## Return results
        return results
    server.register_function(airpollution_function, 'pollution')

    ## Run the server's main loop
    server.serve_forever()
