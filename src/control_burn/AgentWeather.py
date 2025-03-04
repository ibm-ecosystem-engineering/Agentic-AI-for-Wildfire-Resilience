import os
from crewai import Agent, Task, Crew
from langchain.tools import Tool

from dotenv import load_dotenv
import json
import requests

#### Here’s a simple CrewAI example using IBM Watsonx.ai LLM with two agents. Each agent independently calls the Watson LLM to process different tasks.

import logging

from llm.LlmMain import LlmMain
from util.DictionaryUtil import DictionaryUtil

from CommonConstants import *

class AgentWeather(object):

    def __init__(
        self
    ) -> None:
        load_dotenv()
        self._init_config()

    def _init_config(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(os.environ.get('LOGLEVEL', 'INFO').upper())

    def get_city_coordinates(self, city):
        """Get latitude and longitude of a city using Open-Meteo's geocoding API."""
        url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
        response = requests.get(url)
        
        if response.status_code == 200 and response.json().get("results"):
            data = response.json()["results"][0]
            return data["latitude"], data["longitude"]
        else:
            return None, None
        
    def fetch_weather(self, city):
        """Fetch weather data using Open-Meteo API."""
        lat, lon = self.get_city_coordinates(city)
        if lat is None or lon is None:
            return f"Could not find coordinates for {city}."
        
        self.logger.info(f"latitude : {lat} ")
        self.logger.info(f"longitude : {lon} ")
        
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&current=temperature_2m,humidity_2m,wind_speed_10m"
        response = requests.get(weather_url)

        if response.status_code == 200:

            json_string = json.dumps(response.json())
            self.logger.info(f"Weather API Response : {json_string} ")

            data = response.json()

            weather_data = data["current_weather"]
            result1 = f"Weather in {city}:\n" \
                    f"Temperature: {weather_data['temperature']}°C\n" \
                    f"Wind Speed: {weather_data['windspeed']} km/h\n" \
                    f"Weather Code: {weather_data['weathercode']}"
            self.logger.info(f"Weather API Response : {result1} ")

            result = {
                "temperature": data["current"]["temperature_2m"],
                "humidity": data["current"]["humidity_2m"],
                "wind_speed": data["current"]["wind_speed_10m"]
            }                    

            return result


    def getAgent(self, llm):

        weather_tool = Tool(
            name="get_current_weather",
            func=self.fetch_weather,
            description="Get current weather for a specific city",
        )

        # Create Agent
        weather_agent = Agent(
            role="Weather Data Fetcher",
            goal="Fetch weather data for a given city",
            backstory="An API specialist that retrieves weather data from Weather APIs.",
            tools=[weather_tool],
            llm=llm,
            verbose=True,
            max_iter=1
        )

        return weather_agent
    

    def getTask(self, weather_agent, tasks):

        # Create Task
        weather_task = Task(
            description=f"For the list of cities identified, retrieve current weather data, such as temperature, humidity and wind speed",
            expected_output="Weather data including city, temperature, wind speed and humidity",
            agent=weather_agent,
            retries=0,  # Ensure no automatic retries
            context=tasks  # This task will wait for research_task to complete
        )

        return weather_task

