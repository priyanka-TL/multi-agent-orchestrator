from src.logger import get_logger
from .base import BaseAgent

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
        
    def process(self, request: str, history: list = None) -> str:
        logger.info(f"[{self.name}] Generating conversational response...")
        response = self.llm_client.chat_completion(
            system_prompt=self.system_prompt, 
            user_prompt=request, 
            history=history,
            temperature=0.7
        )
        return response or "I'm having trouble coming up with a tip right now. Please try again!"

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
        
    def process(self, request: str, history: list = None) -> str:
        logger.info(f"[{self.name}] Generating conversational response...")
        response = self.llm_client.chat_completion(
            system_prompt=self.system_prompt, 
            user_prompt=request, 
            history=history,
            temperature=0.3
        )
        return response or "I'm having trouble diagnosing that. Please try again!"

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
        
    def process(self, request: str, history: list = None) -> str:
        logger.info(f"[{self.name}] Generating conversational response...")
        response = self.llm_client.chat_completion(
            system_prompt=self.system_prompt, 
            user_prompt=request, 
            history=history,
            temperature=0.5
        )
        return response or "I'm having trouble answering that. Please try again later."
