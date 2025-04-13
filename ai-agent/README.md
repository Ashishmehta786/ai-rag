# Multi-Agent Coding System

A powerful multi-agent system built with LangChain and Google Gemini 1.5 Pro for coding assistance, **API** documentation search, and code generation.

## Features

- **Coding Agent**: Expert coding assistant powered by Gemini 1.5 Pro
- **Web **Scraping****: Extract information from websites and API documentation
- **Code Generation**: Generate code based on requirements
- **Multi-Agent Architecture**: Extensible system for adding more specialized agents
- **Vector Store Integration**: Store and retrieve information from uploaded documents

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your API keys:
   ```
   GOOGLE_API_KEY=your_gemini_api_key
   USER_AGENT=your_user_agent
   ```
4. Run the server:
   ```bash
   python main.py
   ```

## API Endpoints

### Query the Coding Agent

```
POST /query
```

Request body:
```json
{
  "query": "Create a React hook for handling API calls",
  "agent_type": "coding"
}
```

### Search API Documentation

```
POST /search-api-docs
```

Request body:
```json
{
  "query": "useState",
  "api_url": "https://reactjs.org/docs/hooks-reference.html"
}
```

### Extract Code Examples

```
POST /extract-code
```

Request body:
```json
{
  "url": "https://reactjs.org/docs/hooks-custom.html"
}
```

### Upload Files

```
POST /upload
```

Form data:
- `file`: The file to upload

## Testing

There are two ways to run the tests:

### Option 1: Run the server and tests separately

1. Start the server:
   ```bash
   python main.py
   ```

2. In a separate terminal, run the tests:
   ```bash
   python test_agent.py
   ```

### Option 2: Run everything with a single command

```bash
python run_test.py
```

This will start the server, run the tests, and then shut down the server automatically.

## Architecture

The system consists of:

1. **MultiAgentSystem**: Routes requests to appropriate agents
2. **CodingAgent**: Handles coding-related queries
3. **WebTools**: Provides web scraping and API documentation search capabilities
4. **FastAPI Server**: Exposes REST API endpoints

## Extending the System

To add a new agent:

1. Create a new agent class in `agent/multi_agent.py`
2. Add the agent to the `agents` dictionary in the `MultiAgentSystem` class
3. Create appropriate tools for the agent

## License

MIT 