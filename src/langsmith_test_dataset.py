import os
import dotenv
from react_agent import invoke
from test_agent import extract_agent_answer

dotenv.load_dotenv("../.env")

from langsmith import Client

client = Client()

dataset_name = "question_about_movies_dataset_2"

test_dataset = [
    {
        "inputs": {"question": "What are the top 10 highest rated movies?"},
        "outputs": {
            "answer_include": ["Little Big Top", "Dancer", "Texas Pop. 81", "Me You and Five Bucks"],
            "tool_calls": ['sql_db_query']}
    },
    {
        "inputs": {"question": "Which country the movie 15 Minutes was produced?"},
        "outputs": {
            "answer_include": ["Germany"],
            "tool_calls": ['sql_db_query']}
    },
    {
        "inputs": {"question": "How many movies are there in the database?"},
        "outputs": {
            "answer_include": ["4803"],
            "tool_calls": ['sql_db_query']}
    },
    {
        "inputs": {"question": "How many movies were producted in Germany?"},
        "outputs": {
            "answer_include": ["324"],
            "tool_calls": ['sql_db_query']}
    },
    {
        "inputs": {"question": "What country was the movie 2 Guns produced?"},
        "outputs": {
            "answer_include": ["United States of America"],
            "tool_calls": ['sql_db_query']}
    },
    {
        "inputs": {"question": "What data is stored in the database?"},
        "outputs": {
            "answer_include": ["movies", "production countries", "genres"],
            "tool_calls": ['sql_db_list_tables']}
    }
]

# Create dataset if it doesn't exist
if not client.has_dataset(dataset_name=dataset_name):
    dataset = client.create_dataset(
        dataset_name=dataset_name, 
        description="A dataset of questions about movies and their answers."
    )
    # Add examples to the dataset
    client.create_examples(dataset_id=dataset.id, examples=test_dataset)

def target_function(inputs) -> dict:
    result = invoke(inputs["question"])
    return extract_agent_answer(result["messages"])

def answer_evaluator(outputs: dict, reference_outputs: dict) -> bool:
    answer_matches = any(answer.lower() in outputs["answer"].lower() for answer in reference_outputs["answer_include"])
    
    if answer_matches:
        return True
    else:
        return False

def tool_calls_evaluator(outputs: dict, reference_outputs: dict) -> bool:
    tool_calls_match = any(tool_call in outputs["tool_calls"] for tool_call in reference_outputs["tool_calls"])
    
    if tool_calls_match:
        return True
    else:
        return False



experiment_results = client.evaluate(
    target_function, 
    data=dataset_name, 
    evaluators=[answer_evaluator, tool_calls_evaluator],
    experiment_prefix="Exp_On_LangSmith", 
    max_concurrency=1,
    )

for result in experiment_results:
    print(result)
        