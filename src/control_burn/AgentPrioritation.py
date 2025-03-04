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

class AgentPrioritation(object):

    def __init__(
        self
    ) -> None:
        load_dotenv()
        self._init_config()

    def _init_config(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(os.environ.get('LOGLEVEL', 'INFO').upper())

        
    def detect_fire(self, temperature, wind_speed, humidity):
        """Detect the fire based on temperature, wind_speed, humidity."""

        result = False
        if (wind_speed > 20 and temperature > 80 and humidity < 26) :
            result = True
        return result

    def detect_fire(self, temperature, humidity, wind_speed):
        fire_risk = temperature > 35 and humidity < 30 and wind_speed > 40
        return "High fire risk detected! Immediate action required." if fire_risk else "Fire risk is low."

    def getAgent(self, llm):
        tool = Tool(
            name="detect_fire",
            func=self.detect_fire,
            description="Detect the fire based on the given temperature, wind_speed, humidity",
        )

        # Create Agent
        agent = Agent(
            role="Fire Risk Detector",
            goal="Analyze weather conditions of the cities and detect fire risks.",
            backstory="An expert in fire behavior who assesses risks based on temperature, humidity, and wind speed.",
            # tools=[tool],
            llm=llm,
            verbose=True,
        )
        return agent
    

    def getTask(self, agent, tasks):
        # Create Task
        task = Task(
            description=f"Analyze weather conditions of the cities based on temperature, humidity, and wind speed and determine fire risk.",
            expected_output="Find out the top 3 cities in the order of the fire risk ",
            agent=agent,
            retries=0,  # Ensure no automatic retries
            context=tasks  # This task will wait for research_task to complete
        )
        return task