import os
from dotenv import load_dotenv
import openai
from langdetect import detect, DetectorFactory, LangDetectException

# ensure deterministic language detection results
DetectorFactory.seed = 0

# use the client-based API from openai>=1.0
from openai import OpenAI

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise RuntimeError("OPENAI_API_KEY environment variable is not set.")

client = OpenAI(api_key=openai.api_key)


def _is_thai(text: str) -> bool:
    """Return True if the text contains Thai characters."""
    for ch in text:
        if "\u0E00" <= ch <= "\u0E7F":
            return True
    return False


def _goal_is_thai(text: str) -> bool:
    """Return True if the text language is detected as Thai."""
    try:
        return detect(text) == "th"
    except LangDetectException:
        return _is_thai(text)

def get_plan(goal: str) -> str:
    """Return a 7-day meal and workout plan for the given goal."""
    thai = _goal_is_thai(goal)
    system_msg = "You are an AI fitness planner."
    system_msg += " Respond in Thai." if thai else " Respond in English."

    user_msg = (
        "Create a 7-day meal plan and workout schedule for the following goal: "
        f"{goal}. Provide the plan in a clear, organized format with each day labeled."
    )


    response = client.chat.completions.create(

        model="gpt-4",
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_msg},
        ],
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()


def evaluate_plan(goal: str, plan: str) -> str:
    """Return short feedback evaluating the given plan."""
    thai = _goal_is_thai(goal)
    system_msg = "You are a fitness coach providing short feedback on a 7-day plan."
    system_msg += " Respond in Thai." if thai else " Respond in English."

    user_msg = (
        f"Goal: {goal}\n\nPlan:\n{plan}\n\n"
        "Give 3 sentences of feedback about whether the plan is realistic, too intense, or unbalanced."
    )

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_msg},
        ],
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()
