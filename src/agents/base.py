from abc import ABC, abstractmethod
from src.llm import LLMClient

class BaseAgent(ABC):
    """
    Abstract base class for all agents.
    Enforces a common interface for processing requests.
    """
    
    def __init__(self, name: str, description: str, system_prompt: str = ""):
        self.name = name
        self.description = description
        self.system_prompt = system_prompt
        self.llm_client = LLMClient()
        
    @abstractmethod
    def process(self, request: str, history: list = None) -> str:
        """
        Process the user's request and return a response.
        Must be implemented by subclasses.
        """
        pass
