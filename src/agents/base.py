from abc import ABC, abstractmethod
from typing import List, Any
from src.llm import get_llm
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage

class BaseAgent(ABC):
    """
    Abstract base class for all agents.
    Enforces a common interface for processing requests using LangChain.
    """
    
    def __init__(self, name: str, description: str, system_prompt: str = "", tools: List[Any] = None):
        self.name = name
        self.description = description
        self.system_prompt = system_prompt
        self.tools = tools or []
        
        # Initialize the LLM
        self.llm = get_llm()
        
        if self.tools:
            # Create a langgraph react agent
            from langgraph.prebuilt import create_react_agent
            self.agent_executor = create_react_agent(self.llm, self.tools, prompt=self.system_prompt)
            self.chain = None
        else:
            # Build the base chain
            prompt = ChatPromptTemplate.from_messages([
                ("system", self.system_prompt),
                ("placeholder", "{history}"),
                ("human", "{request}")
            ])
            self.chain = prompt | self.llm | StrOutputParser()
            self.agent_executor = None
        
    def process(self, request: str, history: list = None) -> str:
        """
        Process the user's request and return a response using the LCEL chain or AgentExecutor.
        """
        try:
            if self.agent_executor:
                messages = []
                if history:
                    for msg in history:
                        if msg.get("role") == "user":
                            messages.append(HumanMessage(content=msg.get("content", "")))
                        else:
                            messages.append(AIMessage(content=msg.get("content", "")))
                
                messages.append(HumanMessage(content=request))
                
                result = self.agent_executor.invoke({"messages": messages})
                return result["messages"][-1].content
            else:
                # Convert existing simple history dicts to LangChain format tuples
                formatted_history = []
                if history:
                    for msg in history:
                        if msg.get("role") == "user":
                            formatted_history.append(("human", msg.get("content", "")))
                        else:
                            formatted_history.append(("ai", msg.get("content", "")))
                            
                return self.chain.invoke({
                    "request": request,
                    "history": formatted_history
                })
        except Exception as e:
            import traceback
            traceback.print_exc()
            return f"I encountered an error processing your request: {str(e)}"
