# AI hydration tracker

A small full-stack project pairing a FastAPI backend with a Streamlit dashboard and an LLM-powered agent that gives personalized hydration feedback based on daily intake.

Built as a portfolio project to demonstrate: API design with FastAPI, LLM integration via LangChain, and a data-driven Streamlit UI backed by SQLite.

## Features

- Log water intake via a REST API or the dashboard UI
- An AI agent (LangChain + OpenAI) analyzes each log and returns a short, personalized hydration comment
- Daily progress ring against a configurable goal
- Streak, average, and best-day stats computed from intake history
- History chart of intake over time

## Architecture

```
Streamlit dashboard  ──┐
                        ├──>  SQLite (intake history)
FastAPI API        ────┘
        │
        └──> LangChain agent ──> OpenAI (gpt-4)
```

- `dashboard.py` — Streamlit front end
- `api.py` — FastAPI routes for logging intake and fetching history
- `agent.py` — LangChain wrapper around the LLM for hydration analysis
- `database.py` — SQLite persistence layer
- `logger.py` — file-based logging for API calls

## Tech stack

Python · FastAPI · Streamlit · LangChain · OpenAI API · SQLite · Plotly · Pandas

## Setup

1. Clone the repo and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Copy `.env.example` to `.env` and add your OpenAI API key:
   ```bash
   cp .env.example .env
   ```
3. Run the API:
   ```bash
   uvicorn src.api:app --reload
   ```
4. Run the dashboard (from inside `src/`):
   ```bash
   cd src
   streamlit run dashboard.py
   ```

## API endpoints

| Method | Path                        | Description                                  |
| ------ | --------------------------- | -------------------------------------------- |
| POST   | `/log_intake`               | Log a water intake entry and get AI feedback |
| GET    | `/intake_history/{user_id}` | Retrieve a user's intake history             |

## What I'd build next

- Push-based reminders (scheduled check for "no intake logged in N hours")
- Swap SQLite for Postgres to support concurrent users
- Add an eval set to measure the quality/consistency of the AI feedback across intake levels

## Screenshots

_Add a screenshot or short GIF of the dashboard here._

## License

MIT
