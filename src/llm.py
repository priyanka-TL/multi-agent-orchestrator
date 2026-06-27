import time
import requests
from typing import Dict, Any, Optional
from src.config import config
from src.logger import get_logger

logger = get_logger("llm_client")

class LLMClient:
    """
    A robust client for making requests to the configured LLM API (Groq or OpenRouter).
    """
    
    def __init__(self):
        self.provider = config.LLM_PROVIDER
        
        if self.provider == "groq":
            self.BASE_URL = "https://api.groq.com/openai/v1/chat/completions"
            self.api_key = config.GROQ_API_KEY
            self.model = config.GROQ_MODEL
        else:
            self.BASE_URL = "https://openrouter.ai/api/v1/chat/completions"
            self.api_key = config.OPENROUTER_API_KEY
            self.model = config.OPENROUTER_MODEL
            
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def chat_completion(self, system_prompt: str, user_prompt: str, history: list = None, temperature: float = 0.0, max_retries: int = 3) -> Optional[str]:
        """
        Sends a request to the LLM and returns the text response.
        Includes a retry mechanism for 429 Too Many Requests errors.
        Returns None if the request ultimately fails.
        """
        messages = [{"role": "system", "content": system_prompt}]
        
        if history:
            messages.extend(history)
            
        messages.append({"role": "user", "content": user_prompt})
        
        data = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature
        }

        for attempt in range(1, max_retries + 1):
            try:
                logger.debug(f"Calling {self.provider} with model: {self.model} (Attempt {attempt}/{max_retries})")
                response = requests.post(
                    self.BASE_URL, 
                    json=data, 
                    headers=self.headers, 
                    timeout=10
                )
                response.raise_for_status()
                
                result = response.json()
                content = result["choices"][0]["message"]["content"].strip()
                return content
                
            except requests.exceptions.Timeout:
                logger.error(f"{self.provider} API request timed out.")
                return None
            except requests.exceptions.RequestException as e:
                if e.response is not None and e.response.status_code == 429:
                    if attempt < max_retries:
                        logger.warning(f"Rate limited (429). Retrying in 3 seconds... (Attempt {attempt}/{max_retries})")
                        time.sleep(3)
                        continue
                        
                logger.error(f"{self.provider} API request failed: {e}")
                if e.response is not None:
                    logger.error(f"Response content: {e.response.text}")
                return None
            except Exception as e:
                logger.exception(f"Unexpected error calling LLM: {e}")
                return None
            
        return None
