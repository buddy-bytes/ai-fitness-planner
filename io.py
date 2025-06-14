def ask_user_goal() -> str:
    """Prompt the user for their fitness goal."""
    return input("What is your fitness goal? (e.g., lose weight, build muscle) ")


def print_plan(plan: str) -> None:
    """Display the generated plan."""
    print("\n7-Day Meal and Workout Plan:\n")
    print(plan)
