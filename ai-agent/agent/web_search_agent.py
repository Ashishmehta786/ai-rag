from typing import List, Dict, Any
from langchain.tools import Tool
from langchain_core.tools import tool
from .base_agent import BaseAgent
import json
import re
import aiohttp
import asyncio
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

class WebSearchAgent(BaseAgent):
    """A specialized agent for searching and retrieving information from the web."""
    
    def __init__(self, temperature: float = 0.3):
        """Initialize the web search agent.
        
        Args:
            temperature: The temperature for the LLM (0.0 to 1.0)
        """
        super().__init__(
            name="Web Search Agent",
            description="A specialized agent for searching and retrieving information from the web.",
            temperature=temperature
        )
        
        self.tools = self._create_tools()
        self.agent = self._create_agent(self._get_system_prompt())
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for the web search agent.
        
        Returns:
            The system prompt
        """
        return """You are an expert web search agent that helps find and retrieve information from the web.
        You can search for specific information, summarize content, and extract relevant details.
        You always verify information from multiple sources when possible.
        You provide accurate and up-to-date information.
        You cite your sources when providing information.
        """
    
    def _create_tools(self) -> List[Tool]:
        """Create the tools for the web search agent.
        
        Returns:
            A list of tools
        """
        @tool
        async def search_web(query: str, num_results: int = 5) -> str:
            """Search the web for information based on a query."""
            try:
                # In a real implementation, this would use a search API like Google, Bing, or DuckDuckGo
                # For now, we'll return a placeholder response
                return f"Found {num_results} results for '{query}' on the web. In a real implementation, this would return actual search results."
            except Exception as e:
                return f"Error searching the web: {str(e)}"
        
        @tool
        async def fetch_webpage(url: str) -> str:
            """Fetch and parse a webpage."""
            try:
                # In a real implementation, this would fetch the webpage and parse it
                # For now, we'll return a placeholder response
                return f"Fetched content from {url}. In a real implementation, this would return the actual webpage content."
            except Exception as e:
                return f"Error fetching webpage: {str(e)}"
        
        @tool
        async def extract_text_from_webpage(url: str) -> str:
            """Extract text content from a webpage."""
            try:
                # In a real implementation, this would fetch the webpage and extract the text
                # For now, we'll return a placeholder response
                return f"Extracted text from {url}. In a real implementation, this would return the actual text content."
            except Exception as e:
                return f"Error extracting text from webpage: {str(e)}"
        
        @tool
        async def summarize_webpage(url: str) -> str:
            """Summarize the content of a webpage."""
            try:
                # In a real implementation, this would fetch the webpage, extract the text, and summarize it
                # For now, we'll return a placeholder response
                return f"Summary of {url}. In a real implementation, this would return an actual summary of the webpage content."
            except Exception as e:
                return f"Error summarizing webpage: {str(e)}"
        
        @tool
        async def extract_links_from_webpage(url: str) -> str:
            """Extract links from a webpage."""
            try:
                # In a real implementation, this would fetch the webpage and extract the links
                # For now, we'll return a placeholder response
                return f"Extracted links from {url}. In a real implementation, this would return the actual links from the webpage."
            except Exception as e:
                return f"Error extracting links from webpage: {str(e)}"
        
        @tool
        async def search_within_website(website_url: str, query: str) -> str:
            """Search for information within a specific website."""
            try:
                # In a real implementation, this would search within the specified website
                # For now, we'll return a placeholder response
                return f"Found results for '{query}' within {website_url}. In a real implementation, this would return actual search results."
            except Exception as e:
                return f"Error searching within website: {str(e)}"
        
        @tool
        async def compare_websites(urls: str) -> str:
            """Compare information from multiple websites."""
            try:
                # Parse the URLs
                url_list = json.loads(urls)
                
                # In a real implementation, this would fetch and compare the content from the specified websites
                # For now, we'll return a placeholder response
                return f"Comparison of {len(url_list)} websites. In a real implementation, this would return an actual comparison of the websites."
            except Exception as e:
                return f"Error comparing websites: {str(e)}"
        
        return [
            Tool(
                name="search_web",
                func=search_web,
                description="Search the web for information based on a query"
            ),
            Tool(
                name="fetch_webpage",
                func=fetch_webpage,
                description="Fetch and parse a webpage"
            ),
            Tool(
                name="extract_text_from_webpage",
                func=extract_text_from_webpage,
                description="Extract text content from a webpage"
            ),
            Tool(
                name="summarize_webpage",
                func=summarize_webpage,
                description="Summarize the content of a webpage"
            ),
            Tool(
                name="extract_links_from_webpage",
                func=extract_links_from_webpage,
                description="Extract links from a webpage"
            ),
            Tool(
                name="search_within_website",
                func=search_within_website,
                description="Search for information within a specific website"
            ),
            Tool(
                name="compare_websites",
                func=compare_websites,
                description="Compare information from multiple websites"
            )
        ] 