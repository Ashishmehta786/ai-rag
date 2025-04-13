# Multi-Agent Coding Assistance System

## Overview

The Multi-Agent Coding Assistance System is designed to aid developers by providing intelligent code generation, API documentation search, and problem-solving capabilities. It leverages both a single-agent system using Retrieval-Augmented Generation (RAG) and a multi-agent system to handle diverse queries efficiently.

## Key Features

- **Single Agent (RAG):** Uses context from retrieved documents to generate accurate and relevant responses.
- **Multi-Agent System:** Routes queries to specialized agents equipped with specific tools.
- **API Endpoints:** Provides a RESTful API for easy integration with other applications.
- **Scalable Architecture:** Designed to support a large number of tools and users.

## Tools Created for the Agent

The multi-agent system currently includes the following tools:

- `algebra`: Solves algebraic equations.
- `solve_math_equations`: Solves mathematical equations.
- `search_api_docs`: Searches API documentation.
- `search_web`: Searches the web for relevant information.
- `get_query_from_vectordatabase`: Retrieves information from a vector database.
- `generate_code`: Generates code snippets based on user queries.

**Note:** The goal is to expand this toolset to at least 500 specialized tools.

## Getting Started

### Prerequisites

- Python 3.9+
- FastAPI
- LangChain
- Google Gemini API Key

### Installation

1. Clone the repository:
   ```bash
   git clone [repository_url]
   cd [repository_directory]