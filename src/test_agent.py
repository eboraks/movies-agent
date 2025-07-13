import pytest
import os, dotenv
from langsmith import testing
from react_agent import invoke

## Load the environment variables for langsmith logging
dotenv.load_dotenv("../.env")


def print_message(message):
    
    if message.type == "human":
        print(f"{'-' * 20} USER {'-' * 20}")
        print(message.content)
    elif message.type == "ai" and message.tool_calls:
        for tool_call in message.tool_calls:
            print(f"{'-' * 20} TOOL CALL {'-' * 20}")
            print("Tool call:", tool_call["name"], tool_call["args"])
    elif message.type == "tool":
        print(f"{'-' * 20} TOOL RESULT {'-' * 20}")
        print(message.content)
    elif message.type == "ai" and not message.tool_calls:
        print(f"{'-' * 20} AGENT ANSWER {'-' * 20}") 
        print(message.content)
    else:
        print("Unknown message type:", message.type)

    print("\n")

def extract_agent_answer(messages) -> dict:

    result = {'tool_calls': [], 'answer': None}
    for message in messages:
        if message.type == "ai" and message.tool_calls:
            for tool_call in message.tool_calls:
                result["tool_calls"].append(tool_call["name"])
        elif message.type == "ai" and not message.tool_calls:
            result["answer"] = message.content
    return result


test_data = [
    {
        "question": "What are the top 10 highest rated movies?",
        "answer_include": ["Little Big Top", "Dancer", "Texas Pop. 81", "Me You and Five Bucks"],
        "tool_calls": ['sql_db_query']
    }
]

@pytest.mark.langsmith
@pytest.mark.parametrize("test_case", test_data)
def test_text_to_sql_agent(test_case):
    
    
    # We can use the stream method to stream the output of the agent
    result = invoke(test_case["question"])
    
    agent_answer = extract_agent_answer(result["messages"])

    testing.log_inputs({"question": test_case["question"]})
    testing.log_outputs(agent_answer)

    answer_matches = any(answer.lower() in agent_answer["answer"].lower() for answer in test_case["answer_include"])
    assert answer_matches
    assert any(tool_call in agent_answer["tool_calls"] for tool_call in test_case["tool_calls"])
    