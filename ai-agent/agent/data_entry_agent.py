from typing import List, Dict, Any
from langchain.tools import Tool
from langchain_core.tools import tool
from .base_agent import BaseAgent
import json
import re

class DataEntryAgent(BaseAgent):
    """A specialized agent for handling structured data entry and validation."""
    
    def __init__(self, temperature: float = 0.3):
        """Initialize the data entry agent.
        
        Args:
            temperature: The temperature for the LLM (0.0 to 1.0)
        """
        super().__init__(
            name="Data Entry Agent",
            description="A specialized agent for handling structured data entry and validation.",
            temperature=temperature
        )
        
        self.tools = self._create_tools()
        self.agent = self._create_agent(self._get_system_prompt())
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for the data entry agent.
        
        Returns:
            The system prompt
        """
        return """You are an expert data entry agent that helps with structured data entry and validation.
        You are precise, accurate, and follow strict data validation rules.
        Always verify data before entering it.
        If data is invalid or missing, ask for clarification.
        Format data according to the specified schema.
        """
    
    def _create_tools(self) -> List[Tool]:
        """Create the tools for the data entry agent.
        
        Returns:
            A list of tools
        """
        @tool
        async def validate_data(data: str, schema: str) -> str:
            """Validate data against a JSON schema."""
            try:
                data_dict = json.loads(data)
                schema_dict = json.loads(schema)
                # In a real implementation, this would use a JSON schema validator
                return "Data is valid according to the schema."
            except json.JSONDecodeError:
                return "Invalid JSON data or schema."
            except Exception as e:
                return f"Error validating data: {str(e)}"
        
        @tool
        async def format_data(data: str, format_type: str) -> str:
            """Format data according to specified type (e.g., CSV, JSON, XML)."""
            try:
                data_dict = json.loads(data)
                if format_type.lower() == "csv":
                    # Convert to CSV format
                    headers = list(data_dict[0].keys())
                    rows = [",".join(str(row[h]) for h in headers) for row in data_dict]
                    return "\n".join([",".join(headers)] + rows)
                elif format_type.lower() == "xml":
                    # Convert to XML format
                    xml = ["<?xml version='1.0' encoding='UTF-8'?>", "<root>"]
                    for item in data_dict:
                        xml.append("  <item>")
                        for key, value in item.items():
                            xml.append(f"    <{key}>{value}</{key}>")
                        xml.append("  </item>")
                    xml.append("</root>")
                    return "\n".join(xml)
                else:
                    return json.dumps(data_dict, indent=2)
            except Exception as e:
                return f"Error formatting data: {str(e)}"
        
        @tool
        async def extract_data(text: str, fields: str) -> str:
            """Extract structured data from text based on specified fields."""
            try:
                fields_list = json.loads(fields)
                result = {}
                for field in fields_list:
                    # Simple regex-based extraction
                    pattern = f"{field}:\\s*([^\\n]+)"
                    match = re.search(pattern, text, re.IGNORECASE)
                    if match:
                        result[field] = match.group(1).strip()
                    else:
                        result[field] = None
                return json.dumps(result, indent=2)
            except Exception as e:
                return f"Error extracting data: {str(e)}"
        
        return [
            Tool(
                name="validate_data",
                func=validate_data,
                description="Validate data against a JSON schema"
            ),
            Tool(
                name="format_data",
                func=format_data,
                description="Format data according to specified type (CSV, JSON, XML)"
            ),
            Tool(
                name="extract_data",
                func=extract_data,
                description="Extract structured data from text based on specified fields"
            )
        ] 