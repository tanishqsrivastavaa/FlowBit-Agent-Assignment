from pydantic import BaseModel
from pydantic_ai import Agent
from pydantic_ai.models.groq import GroqModel
from pydantic_ai.providers.groq import GroqProvider
from dotenv import load_dotenv
import os
from prompts import system_prompt_classifier, system_prompt_json, system_prompt_email

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


classifier_agent = Agent(
    model=GroqModel(model_name="llama-3.3-70b-versatile",
    provider=GroqProvider(api_key=GROQ_API_KEY)),
    system_prompt=system_prompt_classifier,
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



