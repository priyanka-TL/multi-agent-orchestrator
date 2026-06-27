from src.logger import get_logger
from .base import BaseAgent
from src.tools import youtube_search_tool, web_search_tool

logger = get_logger("specialized_agents")

class HealthTipAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Health & Wellness Agent",
            description="Provides general health, fitness, diet, and wellness tips. Does not provide medical diagnoses.",
            system_prompt=(
                "You are a helpful and encouraging Health & Wellness Assistant. "
                "You provide practical fitness, diet, and wellness tips. "
                "Keep your answers extremely short, concise, and easy to read (maximum 2-3 sentences). "
                "Use bullet points if listing things. Never give medical diagnoses; always recommend seeing a doctor for serious issues."
            )
        )

class TechnicalAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Technical Support Agent",
            description="Handles technical issues like bugs, errors, login failures, broken features, and installation problems.",
            system_prompt=(
                "You are a Technical Support Assistant. Guide the user step-by-step to "
                "troubleshoot software bugs, login issues, and installation errors. Be concise and helpful."
            )
        )

class GeneralSupportAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="General Support Agent",
            description="Handles general inquiries, business hours, and fallback for unrecognized requests.",
            system_prompt=(
                "You are a friendly General Support Assistant. Answer general questions, "
                "provide business hours, or politely ask the user to clarify if you don't know the answer."
            )
        )

class ResearchAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Research & Web Agent",
            description="Searches the web and YouTube for information, tutorials, links, and references.",
            system_prompt=(
                "You are a Research Assistant. You have access to tools to search the web and YouTube. "
                "Always use your tools to find accurate, up-to-date links and references when asked. "
                "Format your answers with markdown links (e.g. [Title](URL))."
            ),
            tools=[youtube_search_tool, web_search_tool]
        )
