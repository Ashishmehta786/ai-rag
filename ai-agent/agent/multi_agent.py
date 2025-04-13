from typing import List, Dict, Any
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor,create_tool_calling_agent,AgentType
from langchain.tools import Tool
from langchain.memory import ConversationBufferMemory
from langchain_core.tools import tool
from langchain.agents.format_scratchpad import format_to_openai_functions
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from dotenv import load_dotenv
from langchain_community.utils import math
import os
from tools.math_tool import scipy_general_solver
from db.vectorstore import vector_store
from scipy.integrate import quad
from .coding_agent import CodingAgent
load_dotenv()

# Initialize Gemini
llm=ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=0,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

class MultiAgentSystem:
    def __init__(self):
        self.coding_agent = CodingAgent()
        self.agents = {
            "coding": self.coding_agent
        }

    async def route_request(self, request: str, agent_type: str = "coding") -> Dict[str, Any]:
        """Route a request to the appropriate agent."""
        if agent_type not in self.agents:
            raise ValueError(f"Unknown agent type: {agent_type}")
        
        return await self.agents[agent_type].process_request(request)

# Example usage
if __name__ == "__main__":
    import asyncio
    
    async def main():
        multi_agent = MultiAgentSystem()
        response = await multi_agent.route_request(
            "Create a React hook for handling API calls with error handling and loading states"
        )
        print("Response:", response["response"])
        print("\nThought Process:", response["thought_process"])
    
    asyncio.run(main()) 