import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Choose provider: "groq" or "openrouter"
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "groq").lower()
    
    # Groq Settings
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    
    # OpenRouter Settings
    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "")
    OPENROUTER_MODEL: str = os.getenv("OPENROUTER_MODEL", "meta-llama/llama-3.2-3b-instruct:free")
    
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO").upper()

    @classmethod
    def validate(cls):
        """
        Ensure critical configuration is set based on the selected provider.
        """
        if cls.LLM_PROVIDER == "groq" and not cls.GROQ_API_KEY:
            raise ValueError(
                "LLM_PROVIDER is set to 'groq' but GROQ_API_KEY is missing. "
                "Please set it in your .env file."
            )
        elif cls.LLM_PROVIDER == "openrouter" and not cls.OPENROUTER_API_KEY:
            raise ValueError(
                "LLM_PROVIDER is set to 'openrouter' but OPENROUTER_API_KEY is missing. "
                "Please set it in your .env file."
            )

config = Config()
