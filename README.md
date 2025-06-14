# ai-fitness-planner
AI-powered 7-day clean eating and fitness planner

## Setup

1. Install dependencies (the project now uses `openai>=1.0`):
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

The code uses the client-based API introduced in `openai>=1.0`.
