from pydantic_ai import Agent
from pydantic_ai.models.groq import GroqModel
from pydantic_ai.providers.groq import GroqProvider
from dotenv import load_dotenv
import os
from prompts import system_prompt_classifier, system_prompt_json, system_prompt_email, Classification
from memory import SharedMemory
import asyncio

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")



classifier_agent = Agent(
    model=GroqModel(model_name="llama-3.3-70b-versatile",
    provider=GroqProvider(api_key=GROQ_API_KEY)),
    system_prompt=system_prompt_classifier,
    output_type=Classification #enforcing the json schema
)

json_agent = Agent(
    model=GroqModel(model_name="llama-3.3-70b-versatile",
    provider=GroqProvider(api_key=GROQ_API_KEY)),
    system_prompt=system_prompt_json,
)

email_agent = Agent(
    model=GroqModel(model_name="llama-3.3-70b-versatile",
    provider=GroqProvider(api_key=GROQ_API_KEY)),
    system_prompt=system_prompt_email,
)

memory = SharedMemory()

async def process_input(user_input, source="user"):
    # Classify first
    classifier_result = await classifier_agent.run(user_prompt=user_input)
    classification = classifier_result.output
    print("Classifier Output:", classification)
    memory.log(source, "classification", classification)

    # Routing
    route_to = classification.froute_to
    if route_to == "json_agent":
        agent = json_agent
    elif route_to == "email_agent":
        agent = email_agent
    else:
        print("No suitable agent found for:", route_to)
        return

    # Process with routed agent
    agent_result = await agent.run(user_prompt=user_input)
    print(f"{route_to} Output:", agent_result.output)
    memory.log(source, route_to, agent_result.output)

    # 4. Show memory log
    print("Memory Log:", memory.get_all())

if __name__ == "__main__":
    import sys
    import json

    # For demo: read input from file or stdin
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r") as f:
            user_input = f.read()
    else:
        user_input = input("Paste your input (email, JSON, or text): ")

    asyncio.run(process_input(user_input))
