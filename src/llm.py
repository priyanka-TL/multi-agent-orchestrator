from langchain_openai import ChatOpenAI
from src.config import config
from src.logger import get_logger

logger = get_logger("llm_client")

def get_llm(temperature: float = 0.0) -> ChatOpenAI:
    """
    Returns a configured LangChain Chat model (ChatOpenAI)
    pointing to OpenRouter or Groq via OpenAI compatibility.
    """
    provider = config.LLM_PROVIDER
    
    if provider == "groq":
        base_url = "https://api.groq.com/openai/v1"
        api_key = config.GROQ_API_KEY
        model = config.GROQ_MODEL
    else:
        base_url = "https://openrouter.ai/api/v1"
        api_key = config.OPENROUTER_API_KEY
        model = config.OPENROUTER_MODEL
        
    return ChatOpenAI(
        model=model,
        temperature=temperature,
        openai_api_key=api_key,
        openai_api_base=base_url,
        max_retries=3
    )
