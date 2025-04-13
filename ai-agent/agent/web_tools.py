from typing import List, Dict, Any
import aiohttp
from bs4 import BeautifulSoup
from langchain.tools import Tool
from langchain_core.tools import tool
import asyncio
from urllib.parse import urljoin
import json

class WebTools:
    def __init__(self):
        self.session = None
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    async def init_session(self):
        if not self.session:
            self.session = aiohttp.ClientSession(headers=self.headers)

    async def close_session(self):
        if self.session:
            await self.session.close()
            self.session = None

    async def _fetch_page(self, url: str) -> str:
        """Helper function to fetch a webpage."""
        await self.init_session()
        try:
            async with self.session.get(url) as response:
                if response.status == 200:
                    return await response.text()
                else:
                    return f"Error: Unable to fetch webpage. Status code: {response.status}"
        except Exception as e:
            return f"Error fetching webpage: {str(e)}"

    async def search_api_docs(self, query: str, api_url: str) -> str:
        """Search through API documentation."""
        try:
            html = await self._fetch_page(api_url)
            if html.startswith("Error:"):
                return html
            
            soup = BeautifulSoup(html, 'html.parser')
            
            # Look for common API documentation elements
            # Include article and div elements as React docs often use these
            api_elements = soup.find_all(['article', 'div', 'h1', 'h2', 'h3', 'code', 'pre', 'p'])
            relevant_content = []
            
            # Split query into keywords for better matching
            keywords = query.lower().split()
            
            for element in api_elements:
                text = element.get_text().strip()
                
                # Check if any of the keywords are in the text
                if any(keyword in text.lower() for keyword in keywords):
                    # For article or div elements, try to get the entire section
                    if element.name in ['article', 'div']:
                        # Look for headers within this section
                        headers = element.find_all(['h1', 'h2', 'h3'])
                        for header in headers:
                            relevant_content.append(f"\n### {header.get_text().strip()}")
                        
                        # Look for code examples within this section
                        code_blocks = element.find_all(['pre', 'code'])
                        for block in code_blocks:
                            code = block.get_text().strip()
                            if code:
                                relevant_content.append(f"```jsx\n{code}\n```")
                        
                        # Look for paragraphs within this section
                        paragraphs = element.find_all('p')
                        for p in paragraphs:
                            p_text = p.get_text().strip()
                            if p_text:
                                relevant_content.append(p_text)
                    else:
                        # Handle individual elements as before
                        if element.name in ['h1', 'h2', 'h3']:
                            relevant_content.append(f"\n### {text}")
                        elif element.name == 'code':
                            relevant_content.append(f"`{text}`")
                        elif element.name == 'pre':
                            relevant_content.append(f"```jsx\n{text}\n```")
                        else:
                            relevant_content.append(text)
            
            if relevant_content:
                # Remove duplicates while preserving order
                seen = set()
                filtered_content = []
                for content in relevant_content:
                    if content not in seen:
                        seen.add(content)
                        filtered_content.append(content)
                
                return "\n".join(filtered_content)
            else:
                # If no content found, try to extract examples section
                examples_section = soup.find(id="examples")
                if examples_section:
                    return await self.extract_code_examples(f"{api_url}#examples")
                return f"No relevant API documentation found for query: {query}"
        except Exception as e:
            return f"Error searching API docs: {str(e)}"
        finally:
            await self.close_session()

    async def extract_code_examples(self, url: str) -> str:
        """Extract code examples from a webpage."""
        try:
            html = await self._fetch_page(url)
            if html.startswith("Error:"):
                return html
            
            soup = BeautifulSoup(html, 'html.parser')
            
            # Find code blocks
            code_blocks = soup.find_all(['pre', 'code'])
            code_examples = []
            
            for block in code_blocks:
                code = block.get_text().strip()
                if code:
                    if block.name == 'pre':
                        code_examples.append(f"```\n{code}\n```")
                    else:
                        code_examples.append(f"`{code}`")
            
            if code_examples:
                return "\n\n".join(code_examples)
            else:
                return "No code examples found on the page"
        except Exception as e:
            return f"Error extracting code examples: {str(e)}"
        finally:
            await self.close_session()

    def get_tools(self) -> List[Tool]:
        """Get all web-related tools."""
        return [
            Tool(
                name="search_api_docs",
                func=self.search_api_docs,
                description="Search through API documentation"
            ),
            Tool(
                name="extract_code_examples",
                func=self.extract_code_examples,
                description="Extract code examples from a webpage"
            )
        ]

# Example usage
if __name__ == "__main__":
    async def main():
        web_tools = WebTools()
        
        # Example: Search API docs
        result = await web_tools.search_api_docs(
            "useCallback",
            "https://react.dev/reference/react/useCallback"
        )
        print("API docs search result:", result)
        
        # Example: Extract code examples
        result = await web_tools.extract_code_examples(
            "https://react.dev/reference/react/useCallback#examples"
        )
        print("\nCode examples:", result)
    
    asyncio.run(main()) 