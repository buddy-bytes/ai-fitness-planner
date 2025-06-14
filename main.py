import io_utils as io_module
from core import get_plan

def main():

    goal = io_module.ask_user_goal()
    plan = get_plan(goal)
    io_module.print_plan(plan)

    export = input("\nWould you like to export the plan? (y/n) ").strip().lower()
    if export == "y":
        filename = input("Enter filename (without extension): ").strip()
        fmt = input("Choose format - txt or md [txt]: ").strip().lower() or "txt"
        io_module.export_plan(plan, filename, fmt)



if __name__ == "__main__":
    main()
