from typing import List, Dict, Any, Optional
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor
from langchain.tools import Tool
from langchain.memory import ConversationBufferMemory
from langchain.agents.format_scratchpad import format_to_openai_functions
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from dotenv import load_dotenv
import os

load_dotenv()

class BaseAgent:
    """Base agent class that all specialized agents will inherit from."""
    
    def __init__(self, name: str, description: str, temperature: float = 0.7):
        """Initialize the base agent.
        
        Args:
            name: The name of the agent
            description: A description of what the agent does
            temperature: The temperature for the LLM (0.0 to 1.0)
        """
        self.name = name
        self.description = description
        self.temperature = temperature
        
        # Initialize the LLM
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=temperature,
            convert_system_message_to_human=True,
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )
        
        # Initialize memory
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        # Tools will be initialized by subclasses
        self.tools = []
        self.agent = None
    
    def _create_agent(self, system_prompt: str) -> AgentExecutor:
        """Create an agent with the given system prompt and tools.
        
        Args:
            system_prompt: The system prompt for the agent
            
        Returns:
            An AgentExecutor instance
        """
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])

        llm_with_tools = self.llm.bind(functions=[t.metadata for t in self.tools])
        
        agent = (
            {
                "input": lambda x: x["input"],
                "chat_history": lambda x: x.get("chat_history", ""),
                "agent_scratchpad": lambda x: format_to_openai_functions(
                    x.get("intermediate_steps", [])
                ),
            }
            | prompt
            | llm_with_tools
            | OpenAIFunctionsAgentOutputParser()
        )

        return AgentExecutor(
            agent=agent,
            tools=self.tools,
            memory=self.memory,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=3
        )
    
    async def process_request(self, user_input: str) -> Dict[str, Any]:
        """Process a user request and return the response.
        
        Args:
            user_input: The user's input
            
        Returns:
            A dictionary with the response and thought process
        """
        if not self.agent:
            raise ValueError("Agent not initialized. Call _create_agent first.")
            
        try:
            response = await self.agent.ainvoke({"input": user_input})
            return {
                "response": response["output"],
                "thought_process": response.get("intermediate_steps", [])
            }
        except Exception as e:
            return {
                "error": f"Error processing request: {str(e)}",
                "thought_process": []
            }
    
    def get_tools(self) -> List[Tool]:
        """Get all tools for this agent.
        
        Returns:
            A list of tools
        """
        return self.tools 