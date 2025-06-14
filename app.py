import gradio as gr
from core import get_plan
from io_utils import export_plan
import tempfile


def generate_plan(goal, custom_goal):
    actual_goal = custom_goal if goal == "Custom" else goal
    if not actual_goal:
        raise gr.Error("Please provide a fitness goal.")
    plan = get_plan(actual_goal)
    return plan


def download_plan(plan_text):
    if not plan_text:
        raise gr.Error("No plan to download. Generate one first.")
    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".txt")
    temp.close()
    export_plan(plan_text, temp.name, "txt")
    return temp.name


def toggle_custom(goal):
    return gr.update(visible=goal == "Custom")


with gr.Blocks(css=".container {max-width: 700px; margin: auto;}") as demo:
    gr.Markdown("# AI Fitness Planner", elem_classes="container")

    with gr.Column(elem_classes="container"):
        goal_dropdown = gr.Dropdown(
            ["Lose 3 kg in 30 days", "Tone arms and legs", "Gain muscle mass", "Custom"],
            label="Select your goal",
            value="Lose 3 kg in 30 days",
        )
        custom_input = gr.Textbox(label="Custom goal", visible=False)
        goal_dropdown.change(toggle_custom, goal_dropdown, custom_input)

        generate_btn = gr.Button("Generate Plan")
        plan_output = gr.Textbox(label="Plan", lines=15, interactive=False)
        download_btn = gr.Button("Download Plan")
        file_output = gr.File(label="Download", interactive=False)

        generate_btn.click(generate_plan, [goal_dropdown, custom_input], plan_output)
        download_btn.click(download_plan, plan_output, file_output)

if __name__ == "__main__":
    demo.launch()
