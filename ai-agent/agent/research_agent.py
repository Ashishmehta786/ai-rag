from typing import List, Dict, Any
from langchain.tools import Tool
from langchain_core.tools import tool
from .base_agent import BaseAgent
import math
import re

class ResearchAgent(BaseAgent):
    """A general-purpose research agent that can search, perform math, and code."""
    
    def __init__(self, temperature: float = 0.7):
        """Initialize the research agent.
        
        Args:
            temperature: The temperature for the LLM (0.0 to 1.0)
        """
        super().__init__(
            name="Research Agent",
            description="A general-purpose research agent that can search, perform math, and code.",
            temperature=temperature
        )
        
        self.tools = self._create_tools()
        self.agent = self._create_agent(self._get_system_prompt())
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for the research agent.
        
        Returns:
            The system prompt
        """
        return """You are an expert research agent that can help with a wide range of tasks.
        You have access to search tools, math tools, and coding tools.
        Always provide clear, well-documented answers.
        When using tools, make sure to await their responses.
        If you're not sure about something, use the search tools to find information.
        """
    
    def _create_tools(self) -> List[Tool]:
        """Create the tools for the research agent.
        
        Returns:
            A list of tools
        """
        @tool
        async def search_web(query: str) -> str:
            """Search the web for information."""
            # This is a placeholder. In a real implementation, this would use a search API.
            return f"Found information about {query} on the web."
        
        @tool
        async def search_api_docs(query: str, api_url: str) -> str:
            """Search API documentation for information."""
            # This is a placeholder. In a real implementation, this would use a web scraper.
            return f"Found documentation about {query} at {api_url}."
        
        @tool
        async def calculate(expression: str) -> str:
            """Calculate the result of a mathematical expression."""
            try:
                # Remove any non-math characters for safety
                safe_expr = re.sub(r'[^0-9+\-*/().\s]', '', expression)
                result = eval(safe_expr)
                return f"The result of {expression} is {result}"
            except Exception as e:
                return f"Error calculating {expression}: {str(e)}"
        
        @tool
        async def generate_code(prompt: str) -> str:
            """Generate code based on the given prompt."""
            try:
                response = await self.llm.ainvoke([HumanMessage(content=f"Generate code for: {prompt}")])
                return response.content
            except Exception as e:
                return f"Error generating code: {str(e)}"
        
        return [
            Tool(
                name="search_web",
                func=search_web,
                description="Search the web for information"
            ),
            Tool(
                name="search_api_docs",
                func=search_api_docs,
                description="Search API documentation for information"
            ),
            Tool(
                name="calculate",
                func=calculate,
                description="Calculate the result of a mathematical expression"
            ),
            Tool(
                name="generate_code",
                func=generate_code,
                description="Generate code based on requirements"
            )
        ] 