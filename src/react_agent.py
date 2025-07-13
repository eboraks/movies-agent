import os
import prompts

from langchain_core.prompts import ChatPromptTemplate
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain.chat_models import init_chat_model
from langgraph.prebuilt import create_react_agent

# The API key is loaded from the .env file by langgraph-cli
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Initialize the model
model = init_chat_model(
    model="gemini-2.0-flash",
    model_provider="google-genai",
    api_key=gemini_api_key,
    temperature=0,
)

# Initialize the database and toolkit
db = SQLDatabase.from_uri("sqlite:///movies.db")
toolkit = SQLDatabaseToolkit(db=db, llm=model)

# Define the system prompt
system_prompt = prompts.system_prompt_text_to_sql_with_context.format(
    dialect=db.dialect, top_k=10, context=toolkit.get_context()['table_info']
)


# Create the react agent and assign it to the 'app' variable for the server
app = create_react_agent(
    model=model,
    tools=toolkit.get_tools(),
    prompt=ChatPromptTemplate.from_messages([("system", system_prompt), ("placeholder", "{messages}")]),
)

def invoke(query: str):
    # The config is passed to all nodes in the graph
    config = {"configurable": {"project_name": "movies-agent"}}

    return app.invoke({"messages": [("user", query)]}, config=config)
    
