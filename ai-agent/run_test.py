import subprocess
import sys
import time
import os
from rich.console import Console

console = Console()

def run_server_and_test():
    """Start the server and then run the test script."""
    console.print("[bold green]Starting the AI Agent system...[/bold green]")
    
    # Start the server in a separate process
    server_process = subprocess.Popen(
        [sys.executable, "main.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Wait for the server to start
    console.print("[yellow]Waiting for server to start...[/yellow]")
    time.sleep(5)  # Give the server time to start
    
    # Check if the server is running
    if server_process.poll() is not None:
        console.print("[red]Server failed to start![/red]")
        stdout, stderr = server_process.communicate()
        console.print(f"[red]Server output:[/red]\n{stdout}\n{stderr}")
        return
    
    console.print("[green]Server started successfully![/green]")
    
    try:
        # Run the test script
        console.print("[bold blue]Running tests...[/bold blue]")
        test_process = subprocess.run(
            [sys.executable, "test_agent.py"],
            capture_output=True,
            text=True
        )
        
        # Print test output
        console.print(test_process.stdout)
        if test_process.stderr:
            console.print(f"[red]Test errors:[/red]\n{test_process.stderr}")
        
        if test_process.returncode != 0:
            console.print("[red]Tests failed![/red]")
        else:
            console.print("[green]Tests completed successfully![/green]")
    
    finally:
        # Terminate the server process
        console.print("[yellow]Shutting down server...[/yellow]")
        server_process.terminate()
        try:
            server_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server_process.kill()
        
        console.print("[green]Server shut down.[/green]")

if __name__ == "__main__":
    run_server_and_test() 