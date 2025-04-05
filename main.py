from fastapi import FastAPI, Query
from backend.langgraph_flow import run_ai_agents  # ✅ updated import
  # Load variables from .env into environment
from backend.agents.environment_agent import ask_ollama_for_soil_data




app = FastAPI()

@app.post("/run-agents")
def run_agents(input_data: dict):
    return run_ai_agents(input_data)

