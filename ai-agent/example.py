import asyncio
import aiohttp
import json
from rich.console import Console
from rich.markdown import Markdown

console = Console()

async def example_usage():
    async with aiohttp.ClientSession() as session:
        # Example 1: Query the coding agent
        console.print("[bold blue]Example 1: Query the coding agent[/bold blue]")
        query_data = {
            "query": "Create a React hook for handling API calls with error handling and loading states",
            "agent_type": "coding"
        }
        
        async with session.post("http://localhost:8000/query", json=query_data) as response:
            result = await response.json()
            console.print("[bold green]Response:[/bold green]")
            console.print(Markdown(result.get("response", "No response")))
        
        # Example 2: Search API documentation
        console.print("\n[bold blue]Example 2: Search API documentation[/bold blue]")
        api_docs_data = {
            "query": "useCallback",
            "api_url": "https://react.dev/reference/react/useCallback"
        }
        
        async with session.post("http://localhost:8000/search-api-docs", json=api_docs_data) as response:
            result = await response.json()
            console.print("[bold green]API Docs Search Result:[/bold green]")
            console.print(result.get("result", "No result"))
        
        # Example 3: Extract code examples
        console.print("\n[bold blue]Example 3: Extract code examples[/bold blue]")
        extract_code_data = {
            "url": "https://react.dev/reference/react/useCallback#examples"
        }
        
        async with session.post("http://localhost:8000/extract-code", json=extract_code_data) as response:
            result = await response.json()
            console.print("[bold green]Code Examples:[/bold green]")
            console.print(result.get("result", "No result"))

if __name__ == "__main__":
    asyncio.run(example_usage()) 