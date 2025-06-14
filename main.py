import user_io
from core import get_plan


def main():
    goal = user_io.ask_user_goal()
    plan = get_plan(goal)
    user_io.print_plan(plan)


if __name__ == "__main__":
    main()
