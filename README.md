# AI Fitness Planner

A command line and web application that generates a **7‑day meal and workout plan** using OpenAI. The planner automatically detects whether your goal is written in Thai or English using the `langdetect` library and responds in the same language.

## Setup

1. Install the requirements (requires `openai>=1.0`):

   ```bash
   pip install -r requirements.txt
   ```

2. Create a `.env` file from the sample and add your OpenAI API key:

   ```bash
   cp .env.sample .env
   # edit .env and set OPENAI_API_KEY
   ```

## Command line usage

Run the planner from the terminal:

```bash
python main.py
```

You will be asked to pick a preset goal or enter your own. After the plan is displayed you can choose to export it to a **.txt** or **.md** file.

## Web interface

A simple Gradio UI is available. Launch it with:

```bash
python app.py
```

Select a goal (or choose "กำหนดเอง" for custom text), generate the plan and download it if desired.

The application uses the client‑based OpenAI API introduced in version 1.0.

