from abc import ABC, abstractmethod
from src.llm import get_llm
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

class BaseAgent(ABC):
    """
    Abstract base class for all agents.
    Enforces a common interface for processing requests using LangChain.
    """
    
    def __init__(self, name: str, description: str, system_prompt: str = ""):
        self.name = name
        self.description = description
        self.system_prompt = system_prompt
        
        # Initialize the LLM
        self.llm = get_llm()
        
        # Build the base chain
        prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            ("placeholder", "{history}"),
            ("human", "{request}")
        ])
        
        self.chain = prompt | self.llm | StrOutputParser()
        
    def process(self, request: str, history: list = None) -> str:
        """
        Process the user's request and return a response using the LCEL chain.
        """
        # Convert existing simple history dicts to LangChain format tuples
        formatted_history = []
        if history:
            for msg in history:
                if msg.get("role") == "user":
                    formatted_history.append(("human", msg.get("content", "")))
                else:
                    formatted_history.append(("ai", msg.get("content", "")))
                    
        try:
            return self.chain.invoke({
                "request": request,
                "history": formatted_history
            })
        except Exception as e:
            return f"I encountered an error processing your request: {str(e)}"
