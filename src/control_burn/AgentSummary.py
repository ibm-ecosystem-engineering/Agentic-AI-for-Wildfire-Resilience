from datetime import datetime, timedelta
import logging
import os
import json
from crewai import Agent, Task, Crew
from langchain.tools import Tool
from dotenv import load_dotenv

from util.FileUtil import FileUtil

### Static methods
class AgentSummary :

    """Provides a summary JSON combining firefighting equipments and fire fighter safety guidelines."""

    def __init__(
        self
    ) -> None:
        load_dotenv()
        self._init_config()

    def _init_config(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(os.environ.get('LOGLEVEL', 'INFO').upper())

    def generate_summary(self, fire_fighting_trucks_json, fire_fighting_crews_json):
        trucks_json = json.loads(fire_fighting_trucks_json)
        crews_json = json.loads(fire_fighting_crews_json)
        
        result = {
            "summary": {
                "trucks": trucks_json["trucks"],
                "crews": crews_json["crews"]
            }
        }
        return json.dumps(result, indent=4)
        

    def getAgent(self, llm):

        tool = Tool(
            name="generate_summary_from_json",
            func=self.generate_summary,
            description="Provides a summary JSON combining fire fighting trucks and fire fighter crews.",
        )

        # Create Agent
        agent = Agent(
            role="Summary Generator",
            goal="Create a JSON file from the json data fire fighting trucks and fire fighting crews",
            backstory="A json file generator",
            tools=[tool],
            llm=llm,
            verbose=True,
        )

        return agent
    

    def getTask(self, agent, tasks):

        # Create Task
        task = Task(
            description=f"Create a JSON file from the json data fighting trucks and fire fighting crews",
            expected_output="A json file with the data trucks and crews",
            agent=agent,
            retries=0,  # Ensure no automatic retries
            context=tasks # This task will wait for research_task to complete
        )

        return task
    
