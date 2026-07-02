# NovaAssist: Architecture & Multi-Agent Orchestration Workflow

This document provides a comprehensive, high-level and technical overview of the **NovaAssist** multi-agent system. It is designed to explain the internal workings, tool integrations, orchestration logic, and address common questions for technical leadership and management.

---

## 1. High-Level Overview

**NovaAssist** is a production-ready web application that implements a **Multi-Agent Architecture** using **Python, Flask, and LangChain**. 

Instead of relying on a single, monolithic AI model to handle every user request, NovaAssist delegates tasks to a team of specialized AI "sub-agents" (e.g., a Technical Support Agent, a Health & Wellness Agent, and a Research Agent). A central "Orchestrator" intelligently analyzes the user's intent and routes the query to the most appropriate sub-agent.

### Core Technologies Used
*   **Flask:** Provides the backend web server and API endpoints.
*   **LangChain & LCEL (LangChain Expression Language):** The core framework used to build prompt templates, manage LLM interactions, and construct the agent pipelines.
*   **OpenRouter / Groq (via `langchain-openai`):** The LLM provider powering the intelligence behind the orchestrator and the sub-agents.
*   **DuckDuckGo Search (`ddgs`):** Used as external tools by the Research Agent to perform live web and YouTube searches.
*   **Vanilla JS/HTML/CSS:** For a dynamic frontend UI with theming (Light/Dark mode) and direct agent communication capabilities.

---

## 2. How Agent Orchestration Works

The orchestration process is dynamic and **does not rely on hardcoded "if-then-else" logic**. Instead, it uses a zero-shot LLM classification approach.

### Step-by-Step Workflow:
1.  **Incoming Request:** The user submits a message via the frontend UI.
2.  **Target Selection:** 
    *   If the user selects a specific sub-agent from the UI sidebar, the system completely bypasses the orchestrator and sends the message directly to that agent.
    *   If the user selects the default "NovaAssist", the message is passed to the **OrchestratorAgent**.
3.  **Dynamic Intent Classification:** 
    *   The `OrchestratorAgent` takes the user's message and injects it into a classification prompt.
    *   Critically, the orchestrator dynamically builds this prompt by reading the `name` and `description` of every registered sub-agent.
    *   The LLM is instructed: *"Given a user request, classify it into exactly one of the following agent categories based on their descriptions. Only reply with the exact 'Agent Name'."*
4.  **Routing & Delegation:** The orchestrator's LLM outputs the name of the best-suited agent (e.g., "Technical Support Agent"). The orchestrator matches this string to the internal dictionary of agents and routes the request to it.
5.  **Fallback Mechanism:** If the LLM returns an unrecognized agent name, or if an error occurs, the orchestrator defaults to a predefined fallback agent (the "General Support Agent").

---

## 3. How Sub-Agents Process Requests

Once a request reaches a sub-agent, the agent uses LangChain pipelines to generate a response. There are two types of agents in this system:

### A. Simple Agents (No External Tools)
*Examples: Health Tip Agent, Technical Agent, General Support Agent*
*   These agents utilize a straightforward LangChain LCEL chain: `prompt | llm | string_parser`.
*   They rely entirely on their predefined system prompts (which define their persona and boundaries) and the underlying LLM's pre-trained knowledge.
*   They format the conversation history and the new request, send it to the LLM, and return the raw string response.

### B. Tool-Augmented Agents
*Example: Research & Web Agent*
*   These agents are equipped with a list of external tools (e.g., `youtube_search_tool`, `web_search_tool`).
*   **The ReAct (Reasoning + Acting) Loop:** 
    1.  The agent sends the prompt and history to the LLM, informing the LLM of the tools it has available.
    2.  The LLM decides if it needs a tool. If it does, it halts text generation and requests a tool call (e.g., "Search the web for X").
    3.  The agent intercepts this request, executes the actual Python tool (calling the `ddgs` library), and appends the raw search results to the conversation history.
    4.  The LLM is invoked *again*, this time with the search results, allowing it to synthesize a final, factual response.
    5.  To prevent infinite loops, this tool-calling cycle is capped at a maximum of 3 iterations.

---

## 4. External Tools & Integrations

The system currently features two primary external tools (located in `src/tools.py`), both powered by the DuckDuckGo Search API:
1.  **`youtube_search_tool`**: Searches for video tutorials or visual references and returns formatted Markdown links.
2.  **`web_search_tool`**: Performs standard web searches to fetch up-to-date factual information, articles, and references.

These tools are dynamically bound to the LLM (`llm.bind_tools(self.tools)`), meaning the LLM inherently understands their required parameters (like a search query string) and what kind of data they return.

---
