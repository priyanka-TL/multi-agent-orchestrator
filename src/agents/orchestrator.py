from typing import List
from src.logger import get_logger
from src.llm import LLMClient
from .base import BaseAgent
from .specialized import GeneralSupportAgent

logger = get_logger("orchestrator")

class OrchestratorAgent:
    """
    The Main Agent (Router).
    It receives the initial request, queries an LLM to classify the intent based 
    on the available sub-agents' descriptions, and delegates the task.
    """
    def __init__(self, agents: List[BaseAgent], default_agent: BaseAgent = None):
        self.name = "Main Router Agent"
        self.agents = {agent.name: agent for agent in agents}
        self.default_agent = default_agent or GeneralSupportAgent()
        self.llm_client = LLMClient()
        
    def _build_system_prompt(self) -> str:
        """
        Dynamically constructs the system prompt based on the registered agents.
        """
        prompt = (
            "You are a router for a customer support system. "
            "Given a user request, classify it into exactly one of the following agent categories based on their descriptions. "
            "Only reply with the exact 'Agent Name', nothing else.\n\n"
        )
        
        for name, agent in self.agents.items():
            prompt += f"- Agent Name: '{name}'\n  Description: {agent.description}\n"
            
        prompt += f"\nIf none match, reply with '{self.default_agent.name}'."
        return prompt

    def _decide_sub_agent(self, request: str) -> BaseAgent:
        logger.info(f"[{self.name}] Received new user request: '{request}'")
        
        system_prompt = self._build_system_prompt()
        
        logger.debug(f"[{self.name}] Asking LLM to classify intent...")
        category = self.llm_client.chat_completion(system_prompt, request)
        
        if category:
            logger.debug(f"[{self.name}] LLM Output: '{category}'")
            
            # Find the matching agent (case-insensitive for robustness)
            for name, agent in self.agents.items():
                if name.lower() in category.lower():
                    logger.info(f"[{self.name}] Decision: Routing to {name}")
                    return agent
        else:
            logger.warning(f"[{self.name}] LLM failed to return a valid category.")
            
        logger.info(f"[{self.name}] Decision: Routing to {self.default_agent.name} (Fallback)")
        return self.default_agent

    def handle_request(self, request: str, history: list = None) -> dict:
        """
        The entry point for the user request.
        Returns a dictionary with the agent name and the response.
        """
        # Step 1: Decide which sub-agent is best suited
        selected_agent = self._decide_sub_agent(request)
        
        # Step 2: Delegate the request
        response = selected_agent.process(request, history)
        
        # Step 3: Return the response with context
        return {
            "agent_name": selected_agent.name,
            "response": response
        }
