# NovaAssist - Production-Ready Multi-Agent Orchestration

This is a production-style, modular example of a multi-agent routing system in Python. It demonstrates how a Main Agent (Orchestrator) receives a user query, dynamically queries an LLM based on available sub-agents, and delegates the task.

## Key Production Features
1. **No Hardcoding**: The routing logic does not have any hardcoded rules. The `OrchestratorAgent` dynamically constructs prompts using the `name` and `description` of the registered sub-agents.
2. **Modular Architecture**: Code is split into specialized modules (`config`, `logger`, `llm`, `agents`) for easier maintenance and scalability.
3. **Robust API Calls**: The `OpenRouterClient` uses `requests` with timeouts and error handling.
4. **Logging**: Uses Python's standard `logging` module instead of `print()` statements for proper observability.
5. **Environment Configuration**: Uses `python-dotenv` for managing API keys securely.

## Project Structure
- `src/config.py`: Loads environment variables.
- `src/logger.py`: Centralized logging configuration.
- `src/llm.py`: A wrapper for calling OpenRouter API.
- `src/agents/`:
  - `base.py`: The abstract base class for all agents.
  - `specialized.py`: The implementations of our specific sub-agents.
  - `orchestrator.py`: The router logic.
- `app.py`: The Flask web application entry point.
- `templates/` & `static/`: HTML, CSS, and JS for the web interface.

## Requirements
- Python 3.x
- `requests`
- `python-dotenv`
- `flask`

## Setup and Usage

1. **Set up a Virtual Environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment**:
   Copy the example environment file and add your [OpenRouter](https://openrouter.ai/) API key.
   ```bash
   cp .env.example .env
   # Edit .env and set OPENROUTER_API_KEY
   ```

4. **Run the application**:
   ```bash
   python3 app.py
   ```
   
   The web application will be available at `http://127.0.0.1:5000/`.
