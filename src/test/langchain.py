from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

# Set up the OpenAI language model
llm = OpenAI(model_name="gpt-4", temperature=0.7, openai_api_key="your-api-key")

# Define a prompt template
prompt = PromptTemplate(
    input_variables=["question"],
    template="You are a helpful AI assistant. Answer the following question:\n{question}"
)

# Create an LLM chain
chain = LLMChain(llm=llm, prompt=prompt)

# Ask a question
response = chain.run("What is LangChain used for?")
print(response)
