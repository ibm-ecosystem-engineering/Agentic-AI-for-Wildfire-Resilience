import os
from crewai import Agent, Task, Crew, Process
from langchain.tools import Tool

from dotenv import load_dotenv
import json
import requests

#### Here’s a simple CrewAI example using IBM Watsonx.ai LLM with two agents. Each agent independently calls the Watson LLM to process different tasks.

import logging

from llm.LlmMain import LlmMain
from util.DictionaryUtil import DictionaryUtil
from util.FileUtil import FileUtil
from control_burn.AgentAgb import AgentAgb
from control_burn.AgentWeather import AgentWeather
from control_burn.AgentPrioritation import AgentPrioritation
from control_burn.AgentTrucks import AgentTrucks
from control_burn.AgentCrews import AgentCrews
from control_burn.AgentSummary import AgentSummary
from CommonConstants import *

class ControlBurnMain(object):

    def __init__(
        self
    ) -> None:
        load_dotenv()
        self._init_config()

    def _init_config(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(os.environ.get('LOGLEVEL', 'INFO').upper())
        self.fileUtil = FileUtil()
        self.fileUtil.start()

    def invoke(self, payload):
        self.logger.info("invoke started ... ")

        ### Retrive parameters
        file_name_agb = "./data/agb.csv"
        file_name_crews = "./data/crews.csv"
        file_name_trucks = "./data/trucks.csv"

        region_name = payload["input"]

        ### query watsonx model
        llmMain = LlmMain()
        model_id = "watsonx/ibm/granite-3-8b-instruct"
        llm = llmMain.get_watsonx_model_for_agents(model_id)

        # Create Agent
        agentAgb = AgentAgb()
        agb_agent = agentAgb.getAgent(llm)
        agb_task = agentAgb.getTask(agb_agent, file_name_agb, region_name)

        agentWeather = AgentWeather()
        weather_agent = agentWeather.getAgent(llm)
        weather_task = agentWeather.getTask(weather_agent, [agb_task])

        agentPrioritation = AgentPrioritation()
        prioritation_agent = agentPrioritation.getAgent(llm)
        prioritation_task = agentPrioritation.getTask(prioritation_agent, [weather_task])

        agentTrucks = AgentTrucks()
        trucks_agent = agentTrucks.getAgent(llm)
        trucks_task = agentTrucks.getTask(trucks_agent, file_name_trucks, [prioritation_task])

        crewsAgent = AgentCrews()
        crews_agent = crewsAgent.getAgent(llm)
        crews_task = crewsAgent.getTask(crews_agent, file_name_crews, [prioritation_task])

        agentSummary = AgentSummary()
        summary_agent = agentSummary.getAgent(llm)
        summary_task = agentSummary.getTask(summary_agent, [trucks_task, crews_task])

        crew = Crew(
            agents=[
                agb_agent,
                weather_agent,
                prioritation_agent,
                trucks_agent,
                crews_agent,
                summary_agent
            ],
            tasks=[
                agb_task,
                weather_task,
                prioritation_task,
                trucks_task,
                crews_task,
                summary_task
            ],
            process=Process.sequential
        )

        # Execute
        # results = crew.kickoff()
        # print("\nFinal Result:\n", results)
        # result_text = DictionaryUtil.getValue_key1(results.dict(), "raw", None)

        result_text = FileUtil.loadJsonAsObject("./data/sample_output.json")

        resp = {
            "msg" : "Success",
            "result" : result_text
        }
        self.logger.info(f"Response : {resp} ")
        self.logger.info("invoke completed ... ")

        return resp