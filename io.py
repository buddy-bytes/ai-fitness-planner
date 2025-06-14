def ask_user_goal() -> str:
    """Prompt the user to select or enter a fitness goal."""
    options = [
        "Lose 3 kg",
        "Tone arms and legs",
        "Gain muscle",
        "Custom goal",
    ]

    print("Choose your fitness goal:")
    for idx, option in enumerate(options, start=1):
        print(f"  {idx}. {option}")

    choice = input("Enter the number of your choice: ").strip()
    if choice == "4":
        return input("Enter your custom goal: ")

    try:
        choice_idx = int(choice) - 1
        if 0 <= choice_idx < 3:
            return options[choice_idx]
    except ValueError:
        pass

    # Fall back to custom input if selection is invalid
    return input("Enter your fitness goal: ")


def print_plan(plan: str) -> None:
    """Display the generated plan."""
    print("\n7-Day Meal and Workout Plan:\n")
    print(plan)


def export_plan(plan: str, filename: str, format: str = "txt") -> None:
    """Save the plan to a file in the specified format (txt or md)."""
    format = format.lower()
    ext = ".md" if format == "md" else ".txt"
    if not filename.endswith(ext):
        filename += ext

    with open(filename, "w", encoding="utf-8") as f:
        f.write(plan)

    print(f"Plan exported to {filename}")
