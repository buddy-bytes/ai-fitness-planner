import os
import requests
import gradio as gr
import sys
import re

# allow importing modules from the repository root when running this file
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from io_utils import export_plan

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

GOAL_OPTIONS = [
    "ลดน้ำหนัก 3 กิโลใน 30 วัน",
    "ลดพุงและกระชับแขนขา",
    "เพิ่มกล้ามเนื้อแบบ lean",
    "อยากฟิตให้ทันวันแต่งงาน",
]


def _calc_avg_kcal(text: str):
    numbers = re.findall(r"(\d+(?:\.\d+)?)\s*k(?:c|C)al", text)
    if not numbers:
        return None
    total = sum(float(n) for n in numbers)
    return round(total / len(numbers))


def generate_plan(goal: str):
    if not goal.strip():
        raise gr.Error("กรุณาใส่เป้าหมายก่อน")
    resp = requests.post(f"{BACKEND_URL}/generate", json={"goal": goal})
    if resp.status_code != 200:
        raise gr.Error(f"Error: {resp.text}")
    plan = resp.json()["plan"]

    eval_resp = requests.post(
        f"{BACKEND_URL}/evaluate", json={"goal": goal, "plan": plan}
    )
    if eval_resp.status_code != 200:
        raise gr.Error(f"Error: {eval_resp.text}")
    feedback = eval_resp.json()["feedback"]

    avg = _calc_avg_kcal(plan)
    kcal_text = f"📊 ค่าเฉลี่ยแคลอรี่ต่อวัน: {avg} kcal" if avg else ""
    kcal_update = gr.update(value=kcal_text, visible=bool(kcal_text))
    return plan, feedback, kcal_update


def save_plan(plan_text: str) -> str:
    if not plan_text.strip():
        raise gr.Error("ยังไม่มีแผน กรุณาสร้างแผนก่อน")
    import tempfile

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".txt")
    tmp.close()
    export_plan(plan_text, tmp.name, "txt")
    return tmp.name


with gr.Blocks(css=".container {max-width: 700px; margin: auto;}") as demo:
    gr.Markdown("# AI Fitness Planner", elem_classes="container")

    with gr.Column(elem_classes="container"):
        goal_tb = gr.Textbox(label="เป้าหมายของคุณ")
        with gr.Row():
            b1 = gr.Button(GOAL_OPTIONS[0])
            b2 = gr.Button(GOAL_OPTIONS[1])
        with gr.Row():
            b3 = gr.Button(GOAL_OPTIONS[2])
            b4 = gr.Button(GOAL_OPTIONS[3])

        b1.click(lambda: gr.update(value=GOAL_OPTIONS[0]), None, goal_tb, queue=False)
        b2.click(lambda: gr.update(value=GOAL_OPTIONS[1]), None, goal_tb, queue=False)
        b3.click(lambda: gr.update(value=GOAL_OPTIONS[2]), None, goal_tb, queue=False)
        b4.click(lambda: gr.update(value=GOAL_OPTIONS[3]), None, goal_tb, queue=False)

        gen_btn = gr.Button("สร้างแผน")
        plan_box = gr.Textbox(label="แผน 7 วัน", lines=20, interactive=False)
        kcal_md = gr.Markdown(visible=False)
        with gr.Accordion("🧠 ความเห็นจากโค้ช AI", open=False) as acc:
            feedback_md = gr.Markdown()

        copy_btn = gr.Button("📤 คัดลอกแผนเพื่อส่งต่อใน LINE")
        save_btn = gr.Button("บันทึกแผน")
        download_file = gr.File(label="ดาวน์โหลดไฟล์", interactive=False)

        gen_btn.click(generate_plan, [goal_tb], [plan_box, feedback_md, kcal_md])
        save_btn.click(save_plan, plan_box, download_file)
        copy_btn.click(None, plan_box, None, js="(text) => navigator.clipboard.writeText(text)")


if __name__ == "__main__":
    demo.launch()

