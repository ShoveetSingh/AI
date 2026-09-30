import requests
from google import genai
import json
import os
from dotenv import load_dotenv

load_dotenv()

key = os.getenv('API_KEY')

client= genai.Client(api_key=key)

def get_weather(city):
     geo_url = "https://geocoding-api.open-meteo.com/v1/search"

     geo_response = requests.get(
        geo_url,
        params={
            "name": city,
            "count": 1,
            "language": "en",
            "format": "json"
        }
    )

     geo_data = geo_response.json()

     if "results" not in geo_data:
        return {"error": f"Could not find city: {city}"}

     location = geo_data["results"][0]

     latitude = location["latitude"]
     longitude = location["longitude"]

    # Now get actual weather
     weather_url = "https://api.open-meteo.com/v1/forecast"

     weather_response = requests.get(
        weather_url,
        params={
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,relative_humidity_2m,wind_speed_10m"
        }
    )

     weather_data = weather_response.json()

     current = weather_data["current"]

     return {
        "city": city,
        "temperature": current["temperature_2m"],
        "humidity": current["relative_humidity_2m"],
        "wind_speed": current["wind_speed_10m"]
    }

weather_tools={
    'type':'function',
    'name':'get_weather',
    'description':'Get the current weather for the city.',
    'parameters':{
        'type':'object',
        'properties':{
            'city':{
                'type':'string',
                'description':'The name of the city.'
            }
        },
        'required':['city']
    }
}



interaction = client.interactions.create(
    model='gemini-3.8-flash',
    input='whats the weather like in kolkata?',
    tools=[weather_tools]
)

for step in interaction.steps:
    if step.type=='function_call':
        print("\nGemini requested:")
        print("Function:", step.name)
        print("Arguments:", step.arguments)
        result=get_weather(**step.arguments)
        print("\nWeather API returned:")
        print(result)
        final_interaction=client.interactions.create(
           model = 'gemini-3.8-flash',
           previous_interaction_id=interaction.id,
           tools=[weather_tools],
           input=[{
               'type':'function_result',
               'name':step.name,
               'call_id':step.id,
               'result':[
                   {
                       "type": "text",
                            "text": json.dumps(result)
                   }
               ]
           }]
        )
        print("\nGemini's final answer:")
        print(final_interaction.output_text)
