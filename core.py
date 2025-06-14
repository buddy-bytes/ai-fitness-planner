import os
from dotenv import load_dotenv
import openai

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise RuntimeError("OPENAI_API_KEY environment variable is not set.")

def get_plan(goal: str) -> str:
    """Return a 7-day meal and workout plan for the given goal."""
    system_msg = "You are an AI fitness planner."
    user_msg = (
        "Create a 7-day meal plan and workout schedule for the following goal: "
        f"{goal}. Provide the plan in a clear, organized format with each day labeled."
    )

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_msg},
        ],
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()
