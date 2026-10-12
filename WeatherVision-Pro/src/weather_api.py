import requests
from config import API_KEY
from datetime import datetime


BASE_URL = "https://api.openweathermap.org/data/2.5/weather"



def get_weather(city):


    if city.strip() == "":

        return {
            "error": "Please enter city name"
        }



    params = {

        "q": city,

        "appid": API_KEY,

        "units": "metric"

    }



    try:


        response = requests.get(
            BASE_URL,
            params=params,
            timeout=10
        )



        data = response.json()



        # Invalid API key

        if response.status_code == 401:

            return {
                "error":"Invalid API Key"
            }



        # City not found

        if response.status_code == 404:

            return {
                "error":"City not found"
            }



        if response.status_code != 200:

            return {
                "error":"Unable to fetch weather data"
            }



        # Convert sunrise sunset time

        sunrise = datetime.fromtimestamp(
            data["sys"]["sunrise"]
        ).strftime("%I:%M %p")



        sunset = datetime.fromtimestamp(
            data["sys"]["sunset"]
        ).strftime("%I:%M %p")




        weather_data = {


            # Location

            "city":
            data["name"],


            "country":
            data["sys"]["country"],



            "latitude":
            data["coord"]["lat"],



            "longitude":
            data["coord"]["lon"],




            # Temperature

            "temperature":
            data["main"]["temp"],



            "feels":
            data["main"]["feels_like"],



            "min_temp":
            data["main"]["temp_min"],



            "max_temp":
            data["main"]["temp_max"],





            # Weather

            "condition":
            data["weather"][0]["description"].title(),



            "icon":
            data["weather"][0]["icon"],




            # Other details

            "humidity":
            data["main"]["humidity"],



            "pressure":
            data["main"]["pressure"],



            "wind":
            data["wind"]["speed"],



            "clouds":
            data["clouds"]["all"],



            "visibility":
            data.get("visibility",0)//1000,



            # Time

            "sunrise":
            sunrise,



            "sunset":
            sunset


        }



        return weather_data




    except requests.exceptions.Timeout:


        return {

            "error":
            "Network timeout"

        }



    except requests.exceptions.ConnectionError:


        return {

            "error":
            "No internet connection"

        }



    except Exception as e:


        return {

            "error":
            str(e)

        }