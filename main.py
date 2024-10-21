import os
from http.client import responses

from swarm import Swarm, Agent
from dotenv import dotenv_values

secrets = dotenv_values()

# set openai api key as environment variable
os.environ["OPENAI_API_KEY"] = secrets["OPENAI_API_KEY"]

client = Swarm()

if not secrets['OPENWEATHER_API_KEY']:
    print('OPENWEATHER_API_KEY not set')

BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'

# fetch weather data from openweather

def fetch_weather(city_name):
    params = {
        'q': city_name,
        'appid': secrets['OPENWEATHER_API_KEY'],
        'units': 'metric'
    }

    response = requests.get(BASE_URL, params=params)
    weather_data = response.json()

    if response.status_code == 200:
        temperature = weather_data['main']['temp']
        wether_description = weather_data['weather'][0]['description']
        city_name = weather_data['name']

        return f"The weather in {city_name} is {wether_description} with a temperature of {temperature} degrees Celsius."
    else:
        return f"Failed to fetch weather update of {city_name}. Please try again later."


# switch to the weather agent
def transfer_to_weather_agent():
    print(f"Transferring function to weather agent")
    return fetch_weather

# manager agent
manager_agent = Agent(
    name="manager Assistant",
    instructions="You are a helpful manager.You help users by directing them to the right assistant.",
    functions=[transfer_to_weather_agent],
)

#weather agent
weather_agent = Agent(
    name="Weather Assistant",
    instructions="You provide weather information for a given location using the provided tool",
    functions=[fetch_weather],
)

response = client.run(
    agent=manager_agent,
    messages=[{"role": "user", "content": "What is the weather in Dhaka, Bangladesh?"}],
)

print(response.messages[-1]["content"])


# def transfer_to_agent_b():
#     return agent_b
#
#
# agent_a = Agent(
#     name="Agent A",
#     instructions="You are a helpful agent.",
#     functions=[transfer_to_agent_b],
# )
#
# agent_b = Agent(
#     name="Agent B",
#     instructions="Only speak in Haikus.",
# )
#
# response = client.run(
#     agent=agent_a,
#     messages=[{"role": "user", "content": "I want to talk to agent B."}],
# )
#
# print(response.messages[-1]["content"])