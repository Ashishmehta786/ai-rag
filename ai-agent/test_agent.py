import asyncio
import aiohttp
import json
import sys
import time
from rich.console import Console
from rich.markdown import Markdown

console = Console()

async def check_server_running(url="http://localhost:8000", max_retries=3, retry_delay=2):
    """Check if the server is running and return True if it is."""
    for i in range(max_retries):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        return True
        except aiohttp.ClientConnectorError:
            if i < max_retries - 1:
                console.print(f"[yellow]Server not running. Retrying in {retry_delay} seconds... ({i+1}/{max_retries})[/yellow]")
                await asyncio.sleep(retry_delay)
            else:
                console.print("[red]Server is not running. Please start the server with 'python main.py' first.[/red]")
                return False
    return False

async def test_agent():
    # First check if the server is running
    if not await check_server_running():
        console.print("[red]Exiting test. Please start the server first.[/red]")
        return

    async with aiohttp.ClientSession() as session:
        try:
            # Test the query endpoint
            console.print("[bold blue]Testing query endpoint...[/bold blue]")
            query_data = {
                "query": "Create a simple React hook for fetching data",
                "agent_type": "coding"
            }
            
            async with session.post("http://localhost:8000/query", json=query_data) as response:
                result = await response.json()
                console.print("[bold green]Query Response:[/bold green]")
                console.print(Markdown(result.get("response", "No response")))
                
                if "thought_process" in result:
                    console.print("\n[bold yellow]Thought Process:[/bold yellow]")
                    for step in result["thought_process"]:
                        console.print(f"- {step}")
            
            # Test the search-api-docs endpoint
            console.print("\n[bold blue]Testing search-api-docs endpoint...[/bold blue]")
            api_docs_data = {
                "query": "useCallback",
                "api_url": "https://react.dev/reference/react/useCallback"
            }
            
            async with session.post("http://localhost:8000/search-api-docs", json=api_docs_data) as response:
                result = await response.json()
                console.print("[bold green]API Docs Search Result:[/bold green]")
                console.print(result.get("result", "No result"))
            
            # Test the extract-code endpoint
            console.print("\n[bold blue]Testing extract-code endpoint...[/bold blue]")
            extract_code_data = {
                "url": "https://react.dev/reference/react/useCallback#examples"
            }
            
            async with session.post("http://localhost:8000/extract-code", json=extract_code_data) as response:
                result = await response.json()
                console.print("[bold green]Code Examples:[/bold green]")
                console.print(result.get("result", "No result"))
        
        except aiohttp.ClientConnectorError:
            console.print("[red]Error: Could not connect to the server. Make sure it's running.[/red]")
        except Exception as e:
            console.print(f"[red]Error during testing: {str(e)}[/red]")

if __name__ == "__main__":
    console.print("[bold]Starting agent test...[/bold]")
    console.print("[yellow]Note: Make sure the server is running with 'python main.py' first.[/yellow]")
    asyncio.run(test_agent()) 