from datetime import datetime, timedelta
import logging
import os
from crewai import Agent, Task, Crew
from langchain.tools import Tool
from dotenv import load_dotenv

from util.FileUtil import FileUtil

### Static methods
class AgentTrucks :

    def __init__(
        self
    ) -> None:
        load_dotenv()
        self._init_config()

    def _init_config(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(os.environ.get('LOGLEVEL', 'INFO').upper())


    def getAgent(self, llm):

        tool = Tool(
            name="get_truck_details",
            func=FileUtil.csv_to_json,
            description="Get the truck details",
        )

        # Create Agent
        agent = Agent(
            role="Fire Fighting Trucks Provider",
            goal="List essential firefighting truck based on fire risk in JSON format.",
            backstory="A logistics expert who provides the right trucks to fight the wildfires.",
            tools=[tool],
            llm=llm,
            verbose=True,
        )

        return agent
    

    def getTask(self, agent, csv_file_name, tasks):

        # Create Task
        task = Task(
            description=f"Retrieve Fire Fighting Trucks data from the csv file {csv_file_name}.",
            expected_output="list of Fire Fighting Trucks data including SNo,Category,Truck Name in a json data with the key trucks",
            agent=agent,
            retries=0,  # Ensure no automatic retries
            context=tasks  # This task will wait for research_task to complete
        )
        return task
