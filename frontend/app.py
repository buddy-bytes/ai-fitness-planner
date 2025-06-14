import os
import requests
import gradio as gr
import sys

# allow importing modules from the repository root when running this file
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from io_utils import export_plan

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

PRESET_GOALS = [
    "ลดน้ำหนัก 3 กิโลใน 30 วัน",
    "ลดพุงและกระชับแขนขา",
    "เพิ่มกล้ามเนื้อแบบ lean",
    "กำหนดเอง",
]


def generate_plan(selected_goal: str, custom_goal: str) -> str:
    goal = custom_goal if selected_goal == "กำหนดเอง" else selected_goal
    if not goal.strip():
        raise gr.Error("กรุณาใส่เป้าหมายก่อน")
    resp = requests.post(f"{BACKEND_URL}/generate", json={"goal": goal})
    if resp.status_code != 200:
        raise gr.Error(f"Error: {resp.text}")
    return resp.json()["plan"]


def save_plan(plan_text: str) -> str:
    if not plan_text.strip():
        raise gr.Error("ยังไม่มีแผน กรุณาสร้างแผนก่อน")
    import tempfile

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".txt")
    tmp.close()
    export_plan(plan_text, tmp.name, "txt")
    return tmp.name


def toggle_custom(goal: str):
    return gr.update(visible=goal == "กำหนดเอง")


with gr.Blocks(css=".container {max-width: 700px; margin: auto;}") as demo:
    gr.Markdown("# AI Fitness Planner", elem_classes="container")

    with gr.Column(elem_classes="container"):
        goal_dd = gr.Dropdown(PRESET_GOALS, value=PRESET_GOALS[0], label="เลือกเป้าหมาย")
        custom_tb = gr.Textbox(label="ระบุเป้าหมาย", visible=False)
        goal_dd.change(toggle_custom, goal_dd, custom_tb)

        gen_btn = gr.Button("สร้างแผน")
        plan_box = gr.Textbox(label="แผน 7 วัน", lines=20, interactive=False)
        save_btn = gr.Button("บันทึกแผน")
        download_file = gr.File(label="ดาวน์โหลดไฟล์", interactive=False)

        gen_btn.click(generate_plan, [goal_dd, custom_tb], plan_box)
        save_btn.click(save_plan, plan_box, download_file)

if __name__ == "__main__":
    demo.launch()

