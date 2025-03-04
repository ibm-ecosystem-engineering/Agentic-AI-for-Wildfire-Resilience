from datetime import datetime, timedelta
import logging
import os
from crewai import Agent, Task, Crew
from langchain.tools import Tool
from dotenv import load_dotenv

from util.FileUtil import FileUtil

### Static methods
class AgentAgb :

    def __init__(
        self
    ) -> None:
        load_dotenv()
        self._init_config()

    def _init_config(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(os.environ.get('LOGLEVEL', 'INFO').upper())

    # def csv_to_json(slef, csv_file, region, ratings):
    #     data = []

    #     # Read CSV file
    #     with open(csv_file, "r", encoding="utf-8") as file:
    #         csv_reader = csv.DictReader(file)  # Read as dictionary
    #         for row in csv_reader:
    #             data.append(row)

    #     return json.dumps(data, indent=4)  # Return JSON as a string
    

    def getAgent(self, llm):


        tool = Tool(
            name="get_agb_details",
            func=FileUtil.csv_to_json,
            description="Get the agb details from CSV file",
        )

        # Create Agent
        agent = Agent(
            role="AGB Data Fetcher",
            goal="Fetch AGB data",
            backstory="An CSV Data specialist that retrieves AGB data for the given region",
            tools=[tool],
            llm=llm,
            verbose=True,
        )

        return agent
    

    def getTask(self, emp_agent, csv_file_name, region) :

        # Create Task
        task = Task(
            description=f"Retrieve AGB data for from the csv file {csv_file_name} for the given region {region} and given ratings CATASTROPHIC",
            expected_output="List of cities",
            agent=emp_agent
        )

        return task
