# ai-fitness-planner
AI-powered 7-day clean eating and fitness planner

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Copy `.env.sample` to `.env` and add your OpenAI API key:
   ```bash
   cp .env.sample .env
   # then edit .env and set OPENAI_API_KEY
   ```

3. Run the planner:
   ```bash
   python main.py
   ```

During execution you'll be asked to choose a goal from presets or enter a custom one.
After the plan is displayed you can optionally export it to a `.txt` or `.md` file.

## Web Interface

Run the Gradio app instead of the CLI to get a web interface:

```bash
python app.py
```

Select a preset goal or choose **Custom** to enter your own. Generate the plan and optionally download it as a `.txt` file.
