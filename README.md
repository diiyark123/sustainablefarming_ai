# Sustainable Farming - Multi-Agent AI System

This project is a multi-agent AI system designed to support sustainable farming using LangGraph and FastAPI. The system consists of four main agents:

1. **Market Researcher Agent**: Suggests high-demand, profitable crops.
2. **Farmer Advisor Agent**: Provides advice on crop rotation, fertilizers, and planting techniques.
3. **Weather Agent**: Offers weather predictions and seasonal suitability.
4. **Soil & Environment Agent**: Analyzes soil type and recommends suitable crops or actions.

All agents are coordinated using **LangGraph**, and the system uses **Ollama LLMs** for agent responses. A **FastAPI** server powers the backend, and **SQLite** is used for long-term memory.

---

## 🔧 Technologies Used

- **LangGraph**: For building multi-agent workflows
- **Ollama LLMs**: For generating intelligent agent responses
- **FastAPI**: Backend server
- **VS Code**: Development environment

---

## 🚀 How It Works

1. User sends a request to the FastAPI endpoint `/run-agents` with input data.
2. The `run_ai_agents()` function runs all agents sequentially using LangGraph.
3. Each agent processes data and adds their insight.
4. A combined response is returned to the user.

---

## 📁 Project Structure

```
Sustainable_Farming/
├── agents/
│   ├── market_researcher.py
│   ├── farmer_advisor.py
│   ├── weather_agent.py
│   └── environment_agent.py
├── graph.py
├── main.py
├── memory/
│   └── db.sqlite
├── .gitignore
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup Instructions

1. **Clone the repo:**
```bash
git clone https://github.com/yourusername/Sustainable_Farming.git
cd Sustainable_Farming
```

2. **Create virtual environment:**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install requirements:**
```bash
pip install -r requirements.txt
```

4. **Run the API server:**
```bash
uvicorn main:app --reload --port 8000
```

---

## 🧪 Sample API Request

POST to: `http://localhost:8000/run-agents`

```json
{
  "query": "I want to grow crops in Tamil Nadu. I have clay soil and it's May."
}
```

---

## 🙌 Contributions

Open to improvements and suggestions! Feel free to fork and make a pull request.

---

## 📜 License

MIT License
