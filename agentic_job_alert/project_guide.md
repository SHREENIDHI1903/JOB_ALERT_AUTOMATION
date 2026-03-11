# 📖 Project Guide: Agentic Job Alert System

This guide provides a deep dive into the architecture and internal workings of the Agentic Job Alert system.

---

## 🏗️ Architecture Overview

The system is designed as a modular pipeline:
1. **User Interface (Streamlit)**: Collects search terms and natural language preferences.
2. **Scraper (Playwright/BeautifulSoup)**: Extracts job data from LinkedIn without requiring an API key.
3. **AI Agent (Ollama)**: Evaluates each job card against the user's criteria.
4. **Storage (SQLite)**: Persists jobs, scores, and AI-generated explanations.

---

## 🧠 The Agentic Engine (`agent_logic.py`)

The core innovation is the `JobAgent` class. Unlike traditional filters, it uses a local LLM to perform "Reasoning over Data."

### Prompt Strategy
The agent is given a specific prompt that forces it to act as a career assistant. It outputs structured JSON, which allows the Streamlit UI to display scores and explanations cleanly.

---

## 🕷️ Resilient Scraping (`scraper.py`)

LinkedIn frequently changes its CSS classes. To handle this, `scraper.py` uses:
- **Multiple Selector Fallbacks**: It tries several common LinkedIn job card patterns.
- **Human-like Interaction**: Uses `playwright` with random delays and scrolling to simulate real user behavior.
- **Windows Async Patch**: A custom fix for `asyncio` is included to prevent `NotImplementedError` on Windows systems.

---

## 🗄️ Persistence (`storage.py`)

The database (`jobs_agentic.db`) uses a schema that stores:
- **Metadata**: Title, Company, Location, Link.
- **AI Output**: Numerical score (0-10) and a justifying explanation.
- **Uniqueness**: The job link is used as a unique constraint to prevent duplicate processing.

---

## 🔧 Troubleshooting

### Port Issues
If you see `Port 8501 is busy`, you can specify a different port:
```bash
streamlit run app.py --server.port 8503
```

### Ollama Connectivity
Ensure the Ollama server is running (check your taskbar or run `ollama serve`). If the model isn't found, use `ollama list` to verify you have the model specified in `app.py`.

### PowerShell Script Errors
If you get a security error when activating the venv, run this command to allow scripts for your current session:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
```
Or, simply use **Command Prompt (cmd)** where this restriction does not apply.
