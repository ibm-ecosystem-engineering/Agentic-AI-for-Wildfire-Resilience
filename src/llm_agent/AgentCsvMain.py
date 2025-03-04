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
from util.FileUtil import FileUtil

from CommonConstants import *

class AgentCsvMain(object):

    def __init__(
        self
    ) -> None:
        load_dotenv()
        self._init_config()

    def _init_config(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(os.environ.get('LOGLEVEL', 'INFO').upper())

    def get_csv_content(self, file_name):
        resp = FileUtil.csv_to_json(file_name)
        return  resp

    def invoke(self, payload):
        self.logger.info("invoke started ... ")

        ### Retrive parameters
        # input = payload["input"]
        input = "./data/emp.csv"

        ### query watsonx model
        llmMain = LlmMain()
        model_id="watsonx/mistralai/mistral-large",
        model_id = "watsonx/ibm/granite-3-8b-instruct"
        llm = llmMain.get_watsonx_model_for_agents(model_id)

        emp_tool = Tool(
            name="get_emp_details",
            func=self.get_csv_content,
            description="Get the employee details",
        )

        # Create Agent
        emp_agent = Agent(
            role="Employee Data Fetcher",
            goal="Fetch Employee data",
            backstory="An CSV Data specialist that retrieves Employee data from Employee file.",
            tools=[emp_tool],
            llm=llm,
            verbose=True,
            allow_delegation=True            
        )

        # Create Task
        emp_task = Task(
            description=f"Retrieve employee data for from the csv file {input}.",
            expected_output="a json file with the employee details including no, name, age and city",
            agent=emp_agent,
            parameters={"file_name": "./data/emp1.csv"}  # Pass city dynamically
        )

        # Create Crew
        emp_crew = Crew(
            agents=[emp_agent],
            tasks=[emp_task]
        )

        # Execute
        results = emp_crew.kickoff()
        result_text = DictionaryUtil.getValue_key1(results.dict(), "raw", None)
        resp = {
            "msg" : "Success",
            "result" : result_text
        }
        print("\nFinal Result:\n", results)

        self.logger.info("invoke completed ... ")

        return resp