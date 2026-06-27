from langchain_openai import ChatOpenAI
from src.config import config
from src.logger import get_logger

logger = get_logger("llm_client")

def get_llm(temperature: float = 0.0) -> ChatOpenAI:
    """
    Returns a configured LangChain Chat model (ChatOpenAI)
    pointing to OpenRouter or Groq via OpenAI compatibility.
    """
    # Check which provider is configured in our .env file
    provider = config.LLM_PROVIDER
    
    # Configure the base URL and API key based on the provider
    if provider == "groq":
        # Groq provides lightning-fast inference for open-source models
        base_url = "https://api.groq.com/openai/v1"
        api_key = config.GROQ_API_KEY
        model = config.GROQ_MODEL
    else:
        # OpenRouter provides access to hundreds of models (including free ones)
        base_url = "https://openrouter.ai/api/v1"
        api_key = config.OPENROUTER_API_KEY
        model = config.OPENROUTER_MODEL
        
    # We use LangChain's ChatOpenAI class because both Groq and OpenRouter 
    # support the standard OpenAI API format (Chat Completions API).
    return ChatOpenAI(
        model=model,
        temperature=temperature,
        openai_api_key=api_key,
        openai_api_base=base_url,
        max_retries=3
    )
