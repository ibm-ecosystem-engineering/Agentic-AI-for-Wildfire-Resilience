from langchain.llms import OpenAI
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool
from langchain.utilities import SerpAPIWrapper

# Set your API keys
OPENAI_API_KEY = "your-openai-api-key"
SERPAPI_API_KEY = "your-serpapi-key"

# Initialize OpenAI model
llm = OpenAI(model_name="gpt-4", temperature=0, openai_api_key=OPENAI_API_KEY)

# Initialize SerpAPI Wrapper for web search
search = SerpAPIWrapper(serpapi_api_key=SERPAPI_API_KEY)

# Define a tool to fetch weather
def get_weather(location):
    """Fetch real-time weather data for a location."""
    query = f"current weather in {location}"
    result = search.run(query)
    return result

# Define a tool in LangChain
weather_tool = Tool(
    name="Weather Checker",
    func=get_weather,
    description="Use this tool to get the current weather for a given location."
)

# Initialize an agent with the weather tool
agent = initialize_agent(
    tools=[weather_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# Ask about the weather
location = "New York"
response = agent.run(f"What is the current weather in {location}?")
print(response)
