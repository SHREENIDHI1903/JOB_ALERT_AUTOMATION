# 🤖 Agentic Job Alert System

A local, AI-powered job search and analysis tool. This project uses **Ollama** to process job descriptions against your personal preferences using natural language.

## 🌟 Features
- **Local LLM**: Powered by Ollama (llama3.2, deepseek-r1, etc.) for private, local analysis.
- **Agentic Filtering**: No hardcoded rules—just describe what you want in plain English.
- **Modern UI**: Interactive dashboard built with Streamlit.
- **Resilient Scraping**: Uses Playwright for robust LinkedIn job extraction.
- **Integrated Storage**: All results are saved in a local SQLite database with AI scores and explanations.

## 🛠️ Setup & Installation

1. **Install Ollama**: Download and install from [ollama.com](https://ollama.com).
2. **Pull a Model**:
   ```bash
   ollama pull llama3.2:3b
   ```
3. **Setup Environment**:
   ```bash
   cd agentic_job_alert
   python -m venv venv
   # In PowerShell, run this first if scripts are disabled:
   # Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
   .\venv\Scripts\activate
   pip install -r requirements.txt
   playwright install chromium
   ```

## 🚀 How to Run
```bash
streamlit run app.py
```
Then open [http://localhost:8502](http://localhost:8502) in your browser.

## 📂 Project Structure
- `app.py`: Streamlit dashboard and main entry point.
- `scraper.py`: Playwright scraping logic.
- `agent_logic.py`: Ollama AI agent implementation.
- `storage.py`: SQLite database management.
- `requirements.txt`: Python dependencies.
