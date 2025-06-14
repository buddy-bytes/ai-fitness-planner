import io as io_module
from core import get_plan


def main():
    goal = io_module.ask_user_goal()
    plan = get_plan(goal)
    io_module.print_plan(plan)


if __name__ == "__main__":
    main()
