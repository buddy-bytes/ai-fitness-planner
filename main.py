import io_utils as io_module
import io as io_module

import user_io

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
