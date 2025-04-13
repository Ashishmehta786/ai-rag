from typing import List, Dict, Any
from langchain.tools import Tool
from langchain_core.tools import tool
from .base_agent import BaseAgent
import re
import ast
import json
import os
import shutil
import logging
import traceback
from pathlib import Path
from langchain_core.messages import HumanMessage
from langchain.memory import ConversationBufferMemory
from langchain.agents import AgentExecutor, create_tool_calling_agent
import aiohttp
import asyncio
from pydantic import BaseModel
# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("coding_agent_debug.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("CodingAgent")
from langchain.tools import StructuredTool



class ProjectInput(BaseModel):
    project_type: str = "fullstack"
    project_name: str = "task-manager"
class CodingAgent(BaseAgent):
    """A specialized agent for code generation, debugging, and analysis with sub-agents for different tasks."""
    
    def __init__(self, temperature: float = 0.2):
        """Initialize the coding agent.
        
        Args:
            temperature: The temperature for the LLM (0.0 to 1.0)
        """
        logger.info("Initializing CodingAgent")
        super().__init__(
            name="Coding Agent",
            description="A specialized agent for code generation, debugging, and analysis.",
            temperature=temperature
        )
        
        # Initialize sub-agents
        logger.info("Initializing sub-agents")
        self.frontend_agent = FrontendAgent()
        self.backend_agent = BackendAgent()
        self.misc_agent = MiscAgent()
        logger.info("Initializing memory")
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        logger.info("Creating tools")
        self.tools = self._create_tools()
        logger.info("Creating agent")
        self.agent = self._create_agent(self._get_system_prompt())
        logger.info("CodingAgent initialization complete")
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for the coding agent.
        
        Returns:
            The system prompt
        """
        logger.debug("Getting system prompt")
        return """You are an expert coding agent that helps with code generation, debugging, and analysis.
        You have specialized sub-agents for frontend, backend, and miscellaneous tasks.
        You can create complete applications with proper file and folder structures.
        You write clean, efficient, and well-documented code.
        You follow best practices and design patterns.
        You can explain your code and reasoning clearly.
        You can debug issues and suggest improvements.
        
        When asked to create a full-stack application:
        1. First use the create_project_structure tool to set up the project structure
        2. Then use generate_frontend_code to create frontend components
        3. Then use generate_backend_code to create backend API endpoints and models
        4. Use create_file to save the generated code to the appropriate files
        5. Provide clear instructions on how to run the application
        
        You can also use the run_in_codesandbox tool to create an interactive sandbox environment where users can see and run the code in real-time. This is especially useful for:
        - Demonstrating how a component works
        - Testing code snippets
        - Providing interactive examples
        - Allowing users to modify and experiment with the code
        
        Always use the available tools to accomplish tasks rather than just providing code snippets.
        You have the capability to create complete applications with proper file structures.
        """
    
    def _create_agent(self, system_prompt: str) -> AgentExecutor:
        """Create the agent with the given system prompt.
        
        Args:
            system_prompt: The system prompt for the agent
            
        Returns:
            The agent executor
        """
        logger.debug("Creating agent with system prompt")
        from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        llm_with_tools = self.llm.bind(tools=self.tools)
        
        agent = create_tool_calling_agent(
            tools=self.tools,
            llm=self.llm,
            prompt=prompt
        )
        
        return AgentExecutor.from_agent_and_tools(
            agent=agent,
            tools=self.tools,
            memory=self.memory,
        )
    
    async def process_request(self, user_input: str) -> Dict[str, Any]:
        """Process a user request and return the response.
        
        Args:
            user_input: The user's input
            
        Returns:
            A dictionary containing the response and thought process
        """
        logger.info(f"Processing request: {user_input}")
        try:
            # Check if the request is for creating a full-stack application
            if "create" in user_input.lower() and ("full-stack" in user_input.lower() or "fullstack" in user_input.lower() or "application" in user_input.lower()):
                logger.info("Detected application creation request")
                
                # Extract project name if provided
                project_name = "task-manager"  # Default name
                project_type = "fullstack"     # Default type
                
                # Try to extract project name
                name_match = re.search(r'name[d\s:]+([a-zA-Z0-9_-]+)', user_input, re.IGNORECASE)
                if name_match:
                    project_name = name_match.group(1)
                    logger.info(f"Extracted project name: {project_name}")
                
                # Try to extract project type
                if "react" in user_input.lower():
                    project_type = "react"
                    logger.info("Detected React project type")
                elif "express" in user_input.lower():
                    project_type = "express"
                    logger.info("Detected Express project type")
                
                logger.info(f"Creating {project_type} project with name: {project_name}")
                
                thought_process = []
                
                try:
                    # Create project structure
                    logger.info(f"Creating project structure for {project_name}")
                    # Call the tool with a single tool_input argument
                    tool_input = {"project_type": "react", "project_name": "task-manager"}
                    print(tool_input)
                    structure_result = await self.tools[5].arun(tool_input)
                    logger.info(f"Project structure created: {structure_result}")
                    thought_process.append(f"Created project structure: {structure_result}")
                except Exception as e:
                    logger.error(f"Error creating project structure: {str(e)}")
                    logger.error(traceback.format_exc())
                    thought_process.append(f"Error creating project structure: {str(e)}")
                    return {
                        "error": f"Failed to create project structure: {str(e)}",
                        "thought_process": thought_process
                    }
                
                # Only proceed with code generation if it's a fullstack or specific type request
                if project_type in ["fullstack", "react", "express"]:
                    try:
                        # Generate frontend code if it's a fullstack or react project
                        if project_type in ["fullstack", "react"]:
                            logger.info("Generating frontend code")
                            frontend_prompt = f"Create a React frontend for a task management application with the following features: task list, task creation form, task details view, and task filtering by category. Include proper state management and API integration."
                            # Call the tool with a single tool_input argument
                            tool_input = {"prompt": frontend_prompt, "framework": "react"}
                            frontend_code = await self.tools[9].arun(tool_input)
                            logger.info("Frontend code generated successfully")
                            thought_process.append("Generated frontend code for task management application")
                            
                            # Create frontend file
                            try:
                                logger.info("Creating frontend file")
                                frontend_path = f"{project_name}/{'src' if project_type == 'react' else 'client/src'}/components/TaskList.js"
                                # Call the tool with a single tool_input argument
                                tool_input = {"file_path": frontend_path, "content": frontend_code}
                                await self.tools[6].arun(tool_input)
                                logger.info(f"Created frontend file: {frontend_path}")
                                thought_process.append(f"Created frontend file: {frontend_path}")
                            except Exception as e:
                                logger.error(f"Error creating frontend file: {str(e)}")
                                logger.error(traceback.format_exc())
                                thought_process.append(f"Error creating frontend file: {str(e)}")
                        
                        # Generate backend code if it's a fullstack or express project
                        if project_type in ["fullstack", "express"]:
                            logger.info("Generating backend code")
                            backend_prompt = f"Create an Express backend for a task management application with the following features: task CRUD operations, MongoDB integration, and proper error handling."
                            # Call the tool with a single tool_input argument
                            tool_input = {"prompt": backend_prompt, "framework": "express"}
                            backend_code = await self.tools[10].arun(tool_input)
                            logger.info("Backend code generated successfully")
                            thought_process.append("Generated backend code for task management application")
                            
                            # Create backend file
                            try:
                                logger.info("Creating backend file")
                                backend_path = f"{project_name}/{'src' if project_type == 'express' else 'server/src'}/models/Task.js"
                                # Call the tool with a single tool_input argument
                                tool_input = {"file_path": backend_path, "content": backend_code}
                                await self.tools[6].arun(tool_input)
                                logger.info(f"Created backend file: {backend_path}")
                                thought_process.append(f"Created backend file: {backend_path}")
                            except Exception as e:
                                logger.error(f"Error creating backend file: {str(e)}")
                                logger.error(traceback.format_exc())
                                thought_process.append(f"Error creating backend file: {str(e)}")
                    except Exception as e:
                        logger.error(f"Error generating code: {str(e)}")
                        logger.error(traceback.format_exc())
                        thought_process.append(f"Error generating code: {str(e)}")
                        # Continue with the response even if code generation fails
                
                # Create a CodeSandbox for the frontend component if it's a fullstack or react project
                codesandbox_result = "CodeSandbox creation skipped."
                if project_type in ["fullstack", "react"] and 'frontend_code' in locals():
                    try:
                        logger.info("Creating CodeSandbox")
                        # Call the tool with a single tool_input argument
                        tool_input = {
                            "code": frontend_code,
                            "language": "react",
                            "dependencies": '{"react": "^18.2.0", "react-dom": "^18.2.0", "axios": "^1.3.5"}'
                        }
                        codesandbox_result = await self.tools[12].arun(tool_input)
                        logger.info(f"CodeSandbox created: {codesandbox_result}")
                        thought_process.append("Created a CodeSandbox for interactive testing of the frontend component")
                    except Exception as e:
                        logger.error(f"Error creating CodeSandbox: {str(e)}")
                        logger.error(traceback.format_exc())
                        thought_process.append(f"Error creating CodeSandbox: {str(e)}")
                        # Continue without CodeSandbox
                
                # Return a comprehensive response
                logger.info("Returning response")
                
                # Customize response based on project type
                if project_type == "react":
                    run_instructions = f"1. Navigate to the project directory: cd {project_name}\n2. Install dependencies: npm install\n3. Start the development server: npm start"
                elif project_type == "express":
                    run_instructions = f"1. Navigate to the project directory: cd {project_name}\n2. Install dependencies: npm install\n3. Start the server: npm run dev"
                else:  # fullstack
                    run_instructions = f"1. Navigate to the project directory: cd {project_name}\n2. Install dependencies: npm run install-all\n3. Start the development servers: npm run dev"
                
                return {
                    "response": f"I've created a {project_type} task management application. The project structure has been set up in the '{project_name}' directory.\n\nTo run the application:\n{run_instructions}\n\nThis will start the development server(s).\n\n{codesandbox_result}",
                    "thought_process": thought_process
                }
            
            # For other requests, use the agent normally
            try:
                logger.info("Using agent for non-application request")
                response = await self.agent.ainvoke({"input": user_input})
                logger.info("Agent response received")
                return {
                    "response": response["output"],
                    "thought_process": response.get("intermediate_steps", [])
                }
            except Exception as e:
                logger.error(f"Error processing request with agent: {str(e)}")
                logger.error(traceback.format_exc())
                return {
                    "error": f"Error processing request with agent: {str(e)}",
                    "thought_process": []
                }
        except Exception as e:
            logger.error(f"Error processing request: {str(e)}")
            logger.error(traceback.format_exc())
            return {
                "error": f"Error processing request: {str(e)}",
                "thought_process": []
            }
    
    def _create_tools(self) -> List[Tool]:
        """Create the tools for the coding agent.
        
        Returns:
            A list of tools
        """
        logger.info("Creating tools")
        
        @tool
        async def generate_code(prompt: str, language: str = "python") -> str:
            """Generate code based on the given prompt and language."""
            logger.debug(f"Generating {language} code for prompt: {prompt[:50]}...")
            try:
                response = await self.llm.ainvoke([HumanMessage(content=f"Generate {language} code for: {prompt}")])
                logger.debug("Code generated successfully")
                return response.content
            except Exception as e:
                logger.error(f"Error generating code: {str(e)}")
                logger.error(traceback.format_exc())
                return f"Error generating code: {str(e)}"
        
        @tool
        async def debug_code(code: str, error_message: str = "") -> str:
            """Debug code and fix issues."""
            logger.debug(f"Debugging code with error message: {error_message[:50] if error_message else 'None'}")
            try:
                if error_message:
                    prompt = f"Debug this code and fix the error: {error_message}\n\nCode:\n{code}"
                else:
                    prompt = f"Review this code for bugs and potential issues:\n{code}"
                
                response = await self.llm.ainvoke([HumanMessage(content=prompt)])
                logger.debug("Code debugging completed")
                return response.content
            except Exception as e:
                logger.error(f"Error debugging code: {str(e)}")
                logger.error(traceback.format_exc())
                return f"Error debugging code: {str(e)}"
        
        @tool
        async def analyze_code(code: str) -> str:
            """Analyze code for quality, complexity, and potential improvements."""
            logger.debug("Analyzing code")
            try:
                # Basic static analysis
                tree = ast.parse(code)
                
                # Count functions and classes
                functions = len([node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)])
                classes = len([node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)])
                
                # Check for common issues
                issues = []
                
                # Check for long functions (more than 50 lines)
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef) and len(node.body) > 50:
                        issues.append(f"Function '{node.name}' is too long ({len(node.body)} lines)")
                
                # Check for global variables
                for node in ast.walk(tree):
                    if isinstance(node, ast.Global):
                        issues.append(f"Global variables used in function '{node.parent.name}'")
                
                # Generate analysis report
                report = {
                    "functions": functions,
                    "classes": classes,
                    "issues": issues,
                    "recommendations": [
                        "Consider adding docstrings to functions and classes",
                        "Break down long functions into smaller ones",
                        "Avoid global variables when possible",
                        "Add type hints for better code clarity"
                    ]
                }
                
                logger.debug("Code analysis completed")
                return json.dumps(report, indent=2)
            except Exception as e:
                logger.error(f"Error analyzing code: {str(e)}")
                logger.error(traceback.format_exc())
                return f"Error analyzing code: {str(e)}"
        
        @tool
        async def refactor_code(code: str, improvements: str = "") -> str:
            """Refactor code to improve quality and maintainability."""
            logger.debug(f"Refactoring code with improvements: {improvements[:50] if improvements else 'None'}")
            try:
                if improvements:
                    prompt = f"Refactor this code with the following improvements: {improvements}\n\nCode:\n{code}"
                else:
                    prompt = f"Refactor this code to improve quality and maintainability:\n{code}"
                
                response = await self.llm.ainvoke([HumanMessage(content=prompt)])
                logger.debug("Code refactoring completed")
                return response.content
            except Exception as e:
                logger.error(f"Error refactoring code: {str(e)}")
                logger.error(traceback.format_exc())
                return f"Error refactoring code: {str(e)}"
        
        @tool
        async def explain_code(code: str) -> str:
            """Explain how the code works in detail."""
            logger.debug("Explaining code")
            try:
                prompt = f"Explain how this code works in detail:\n{code}"
                response = await self.llm.ainvoke([HumanMessage(content=prompt)])
                logger.debug("Code explanation completed")
                return response.content
            except Exception as e:
                logger.error(f"Error explaining code: {str(e)}")
                logger.error(traceback.format_exc())
                return f"Error explaining code: {str(e)}"
        
        @tool(args_schema=ProjectInput)
        async def create_project_structure(project_type: str, project_name: str)->str:
            """ Create a project structure with appropriate folders and files."""
            logger.debug("Creating project structure")
            return f"Created {project_type} project named {project_name}"

    
        # @tool
#         async def create_project_structure(project_type,project_name) -> str:

#             """Create a project structure with appropriate folders and files.
            
#             Args:
#                 project:dict: A dictionary containing project_type and project_name
            
#             Returns:
#                 A string describing the result of the operation
#             """
#             logger.log("this is project_type",project_type)
#             logger.debug(f"Creating {project_type} project structure for {project_name}")
#             try:
#                 # Validate project type
#                 valid_types = ["react", "express", "fullstack"]
#                 if project_type.lower() not in valid_types:
#                     logger.warning(f"Invalid project type: {project_type}. Using default: fullstack")
#                     project_type = "fullstack"
                
#                 # Validate project name
#                 if not project_name or not isinstance(project_name, str):
#                     logger.warning(f"Invalid project name: {project_name}. Using default: task-manager")
#                     project_name = "task-manager"
                
#                 # Sanitize project name
#                 project_name = re.sub(r'[^a-zA-Z0-9_-]', '-', project_name)
#                 if not project_name:
#                     project_name = "task-manager"
                
#                 logger.info(f"Creating project structure with type: {project_type}, name: {project_name}")
                
#                 # Create base directory
#                 base_dir = Path(project_name)
#                 if base_dir.exists():
#                     logger.warning(f"Project directory '{project_name}' already exists.")
#                     return f"Project directory '{project_name}' already exists."
                
#                 base_dir.mkdir(parents=True)
#                 logger.debug(f"Created base directory: {base_dir}")
                
#                 # Create structure based on project type
#                 if project_type.lower() == "react":
#                     # React project structure
#                     logger.debug("Creating React project structure")
#                     (base_dir / "src").mkdir()
#                     (base_dir / "src" / "components").mkdir()
#                     (base_dir / "src" / "pages").mkdir()
#                     (base_dir / "src" / "assets").mkdir()
#                     (base_dir / "src" / "hooks").mkdir()
#                     (base_dir / "src" / "context").mkdir()
#                     (base_dir / "src" / "utils").mkdir()
#                     (base_dir / "src" / "services").mkdir()
#                     (base_dir / "public").mkdir()
                    
#                     # Create basic files
#                     logger.debug("Creating React basic files")
#                     with open(base_dir / "package.json", "w") as f:
#                         f.write('''{
#   "name": "''' + project_name + '''",
#   "version": "0.1.0",
#   "private": true,
#   "dependencies": {
#     "react": "^18.2.0",
#     "react-dom": "^18.2.0",
#     "react-router-dom": "^6.10.0",
#     "axios": "^1.3.5"
#   },
#   "scripts": {
#     "start": "react-scripts start",
#     "build": "react-scripts build",
#     "test": "react-scripts test",
#     "eject": "react-scripts eject"
#   }
# }''')
                    
#                     with open(base_dir / "src" / "index.js", "w") as f:
#                         f.write('''import React from 'react';
# import ReactDOM from 'react-dom/client';
# import App from './App';

# const root = ReactDOM.createRoot(document.getElementById('root'));
# root.render(
#   <React.StrictMode>
#     <App />
#   </React.StrictMode>
# );''')
                    
#                     with open(base_dir / "src" / "App.js", "w") as f:
#                         f.write('''import React from 'react';
# import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

# function App() {
#   return (
#     <Router>
#       <div className="App">
#         <h1>Welcome to ''' + project_name + '''</h1>
#         <Routes>
#           <Route path="/" element={<div>Home Page</div>} />
#         </Routes>
#       </div>
#     </Router>
#   );
# }

# export default App;''')
                    
#                 elif project_type.lower() == "express":
#                     # Express project structure
#                     logger.debug("Creating Express project structure")
#                     (base_dir / "src").mkdir()
#                     (base_dir / "src" / "controllers").mkdir()
#                     (base_dir / "src" / "models").mkdir()
#                     (base_dir / "src" / "routes").mkdir()
#                     (base_dir / "src" / "middleware").mkdir()
#                     (base_dir / "src" / "config").mkdir()
#                     (base_dir / "src" / "utils").mkdir()
                    
#                     # Create basic files
#                     logger.debug("Creating Express basic files")
#                     with open(base_dir / "package.json", "w") as f:
#                         f.write('''{
#   "name": "''' + project_name + '''",
#   "version": "1.0.0",
#   "description": "Express backend application",
#   "main": "src/server.js",
#   "scripts": {
#     "start": "node src/server.js",
#     "dev": "nodemon src/server.js"
#   },
#   "dependencies": {
#     "express": "^4.18.2",
#     "mongoose": "^7.0.3",
#     "dotenv": "^16.0.3",
#     "cors": "^2.8.5",
#     "helmet": "^6.0.1"
#   },
#   "devDependencies": {
#     "nodemon": "^2.0.22"
#   }
# }''')
                    
#                     with open(base_dir / "src" / "server.js", "w") as f:
#                         f.write('''const express = require('express');
# const cors = require('cors');
# const helmet = require('helmet');
# require('dotenv').config();

# const app = express();
# const PORT = process.env.PORT || 5000;

# // Middleware
# app.use(cors());
# app.use(helmet());
# app.use(express.json());

# // Routes
# app.get('/', (req, res) => {
#   res.json({ message: 'Welcome to ''' + project_name + ''' API' });
# });

# // Start server
# app.listen(PORT, () => {
#   console.log(`Server running on port ${PORT}`);
# });''')
                    
#                     with open(base_dir / ".env", "w") as f:
#                         f.write('''PORT=5000
# MONGODB_URI=mongodb://localhost:27017/''' + project_name.lower() + '''
# JWT_SECRET=your_jwt_secret_here''')
                    
#                 elif project_type.lower() == "fullstack":
#                     # Full-stack project structure (React + Express)
#                     logger.debug("Creating full-stack project structure")
#                     (base_dir / "client").mkdir()
#                     (base_dir / "server").mkdir()
                    
#                     # Create client structure (React)
#                     logger.debug("Creating client structure")
#                     (base_dir / "client" / "src").mkdir()
#                     (base_dir / "client" / "src" / "components").mkdir()
#                     (base_dir / "client" / "src" / "pages").mkdir()
#                     (base_dir / "client" / "src" / "assets").mkdir()
#                     (base_dir / "client" / "src" / "hooks").mkdir()
#                     (base_dir / "client" / "src" / "context").mkdir()
#                     (base_dir / "client" / "src" / "utils").mkdir()
#                     (base_dir / "client" / "src" / "services").mkdir()
#                     (base_dir / "client" / "public").mkdir()
                    
#                     # Create server structure (Express)
#                     logger.debug("Creating server structure")
#                     (base_dir / "server" / "src").mkdir()
#                     (base_dir / "server" / "src" / "controllers").mkdir()
#                     (base_dir / "server" / "src" / "models").mkdir()
#                     (base_dir / "server" / "src" / "routes").mkdir()
#                     (base_dir / "server" / "src" / "middleware").mkdir()
#                     (base_dir / "server" / "src" / "config").mkdir()
#                     (base_dir / "server" / "src" / "utils").mkdir()
                    
#                     # Create basic files for client
#                     logger.debug("Creating client basic files")
#                     with open(base_dir / "client" / "package.json", "w") as f:
#                         f.write('''{
#   "name": "''' + project_name + '''-client",
#   "version": "0.1.0",
#   "private": true,
#   "dependencies": {
#     "react": "^18.2.0",
#     "react-dom": "^18.2.0",
#     "react-router-dom": "^6.10.0",
#     "axios": "^1.3.5"
#   },
#   "scripts": {
#     "start": "react-scripts start",
#     "build": "react-scripts build",
#     "test": "react-scripts test",
#     "eject": "react-scripts eject"
#   }
# }''')
                    
#                     # Create basic files for server
#                     logger.debug("Creating server basic files")
#                     with open(base_dir / "server" / "package.json", "w") as f:
#                         f.write('''{
#   "name": "''' + project_name + '''-server",
#   "version": "1.0.0",
#   "description": "Express backend application",
#   "main": "src/server.js",
#   "scripts": {
#     "start": "node src/server.js",
#     "dev": "nodemon src/server.js"
#   },
#   "dependencies": {
#     "express": "^4.18.2",
#     "mongoose": "^7.0.3",
#     "dotenv": "^16.0.3",
#     "cors": "^2.8.5",
#     "helmet": "^6.0.1"
#   },
#   "devDependencies": {
#     "nodemon": "^2.0.22"
#   }
# }''')
                    
#                     # Create root package.json for scripts
#                     logger.debug("Creating root package.json")
#                     with open(base_dir / "package.json", "w") as f:
#                         f.write('''{
#   "name": "''' + project_name + '''",
#   "version": "1.0.0",
#   "description": "Full-stack application",
#   "scripts": {
#     "client": "cd client && npm start",
#     "server": "cd server && npm run dev",
#     "dev": "concurrently \"npm run server\" \"npm run client\"",
#     "install-all": "npm install && cd client && npm install && cd ../server && npm install"
#   },
#   "devDependencies": {
#     "concurrently": "^8.0.1"
#   }
# }''')
                
#                 else:
#                     logger.warning(f"Unknown project type: {project_type}")
#                     return f"Unknown project type: {project_type}. Supported types: react, express, fullstack"
                
#                 logger.info(f"Created {project_type} project structure in '{project_name}' directory.")
#                 return f"Created {project_type} project structure in '{project_name}' directory."
#             except Exception as e:
#                 logger.error(f"Error creating project structure: {str(e)}")
#                 logger.error(traceback.format_exc())
#                 return f"Error creating project structure: {str(e)}"
        
        @tool
        async def create_file(file_path: str, content: str) -> str:
            """Create a file with the given content."""
            logger.debug(f"Creating file: {file_path}")
            try:
                file_path = Path(file_path)
                
                # Create parent directories if they don't exist
                file_path.parent.mkdir(parents=True, exist_ok=True)
                logger.debug(f"Created parent directories: {file_path.parent}")
                
                # Write content to file
                with open(file_path, "w") as f:
                    f.write(content)
                logger.debug(f"Wrote content to file: {file_path}")
                
                return f"Created file: {file_path}"
            except Exception as e:
                logger.error(f"Error creating file: {str(e)}")
                logger.error(traceback.format_exc())
                return f"Error creating file: {str(e)}"
        
        @tool
        async def create_directory(dir_path: str) -> str:
            """Create a directory and its parent directories if they don't exist."""
            logger.debug(f"Creating directory: {dir_path}")
            try:
                dir_path = Path(dir_path)
                dir_path.mkdir(parents=True, exist_ok=True)
                logger.debug(f"Created directory: {dir_path}")
                return f"Created directory: {dir_path}"
            except Exception as e:
                logger.error(f"Error creating directory: {str(e)}")
                logger.error(traceback.format_exc())
                return f"Error creating directory: {str(e)}"
        
        @tool
        async def generate_frontend_code(prompt: str, framework: str = "react") -> str:
            """Generate frontend code using the frontend agent."""
            logger.debug(f"Generating {framework} frontend code for prompt: {prompt[:50]}...")
            try:
                result = await self.frontend_agent.generate_code(prompt, framework)
                logger.debug("Frontend code generated successfully")
                return result
            except Exception as e:
                logger.error(f"Error generating frontend code: {str(e)}")
                logger.error(traceback.format_exc())
                return f"Error generating frontend code: {str(e)}"
        
        @tool
        async def generate_backend_code(prompt: str, framework: str = "express") -> str:
            """Generate backend code using the backend agent."""
            logger.debug(f"Generating {framework} backend code for prompt: {prompt[:50]}...")
            try:
                result = await self.backend_agent.generate_code(prompt, framework)
                logger.debug("Backend code generated successfully")
                return result
            except Exception as e:
                logger.error(f"Error generating backend code: {str(e)}")
                logger.error(traceback.format_exc())
                return f"Error generating backend code: {str(e)}"
        
        @tool
        async def generate_misc_code(prompt: str) -> str:
            """Generate miscellaneous code using the misc agent."""
            logger.debug(f"Generating miscellaneous code for prompt: {prompt[:50]}...")
            try:
                result = await self.misc_agent.generate_code(prompt)
                logger.debug("Miscellaneous code generated successfully")
                return result
            except Exception as e:
                logger.error(f"Error generating miscellaneous code: {str(e)}")
                logger.error(traceback.format_exc())
                return f"Error generating miscellaneous code: {str(e)}"
        
        @tool
        async def run_in_codesandbox(code: str, language: str = "javascript", dependencies: str = "") -> str:
            """Run code in a CodeSandbox environment and return the results.
            
            Args:
                code: The code to run
                language: The programming language (javascript, python, etc.)
                dependencies: JSON string of dependencies to include
                
            Returns:
                The result of running the code
            """
            logger.debug(f"Running code in CodeSandbox with language: {language}")
            try:
                # Validate inputs
                if not code or not isinstance(code, str):
                    logger.error("Invalid code provided")
                    return "Error: Invalid code provided"
                
                # Prepare the sandbox configuration
                sandbox_config = {
                    "files": {
                        "index.js": {
                            "content": code,
                            "isBinary": False
                        }
                    },
                    "template": "node",
                    "dependencies": {}
                }
                
                # Add dependencies if provided
                if dependencies:
                    try:
                        deps = json.loads(dependencies)
                        sandbox_config["dependencies"] = deps
                        logger.debug(f"Added dependencies: {deps}")
                    except json.JSONDecodeError:
                        logger.error("Invalid dependencies JSON format")
                        return "Error: Invalid dependencies JSON format"
                
                # Set template based on language
                if language.lower() == "python":
                    sandbox_config["template"] = "python"
                    sandbox_config["files"] = {
                        "main.py": {
                            "content": code,
                            "isBinary": False
                        }
                    }
                    logger.debug("Set template to python")
                elif language.lower() == "react":
                    sandbox_config["template"] = "react"
                    sandbox_config["files"] = {
                        "src/App.js": {
                            "content": code,
                            "isBinary": False
                        }
                    }
                    logger.debug("Set template to react")
                
                # Create a sandbox using the CodeSandbox API
                try:
                    logger.debug("Sending request to CodeSandbox API")
                    async with aiohttp.ClientSession() as session:
                        async with session.post(
                            "https://codesandbox.io/api/v1/sandboxes/define?json=1",
                            json=sandbox_config,
                            timeout=30  # Add timeout
                        ) as response:
                            if response.status != 200:
                                error_text = await response.text()
                                logger.error(f"Error creating sandbox: {error_text}")
                                return f"Error creating sandbox: {error_text}"
                            
                            try:
                                sandbox_data = await response.json()
                                sandbox_id = sandbox_data.get("sandbox_id")
                                
                                if not sandbox_id:
                                    logger.error("Failed to get sandbox ID")
                                    return "Error: Failed to get sandbox ID"
                                
                                # Get the sandbox URL
                                sandbox_url = f"https://codesandbox.io/embed/{sandbox_id}?fontsize=14&hidenavigation=1&theme=dark"
                                logger.info(f"CodeSandbox created successfully: {sandbox_url}")
                                
                                return f"CodeSandbox created successfully! You can view and run the code at: {sandbox_url}\n\nThis sandbox allows you to see the code in action and make modifications as needed."
                            except Exception as json_error:
                                logger.error(f"Error parsing sandbox response: {str(json_error)}")
                                logger.error(traceback.format_exc())
                                return f"Error parsing sandbox response: {str(json_error)}"
                except aiohttp.ClientError as http_error:
                    logger.error(f"Error connecting to CodeSandbox API: {str(http_error)}")
                    logger.error(traceback.format_exc())
                    return f"Error connecting to CodeSandbox API: {str(http_error)}"
                except asyncio.TimeoutError:
                    logger.error("Timeout connecting to CodeSandbox API")
                    return "Error: Timeout connecting to CodeSandbox API. Please try again later."
            except Exception as e:
                logger.error(f"Error running code in CodeSandbox: {str(e)}")
                logger.error(traceback.format_exc())
                return f"Error running code in CodeSandbox: {str(e)}"
        
        logger.info("All tools created successfully")
        return [
            Tool(
                name="generate_code",
                func=generate_code,
                description="Generate code based on the given prompt and language"
            ),
            Tool(
                name="debug_code",
                func=debug_code,
                description="Debug code and fix issues"
            ),
            Tool(
                name="analyze_code",
                func=analyze_code,
                description="Analyze code for quality, complexity, and potential improvements"
            ),
            Tool(
                name="refactor_code",
                func=refactor_code,
                description="Refactor code to improve quality and maintainability"
            ),
            Tool(
                name="explain_code",
                func=explain_code,
                description="Explain how the code works in detail"
            ),
            
            Tool(
                name="create_project_structure",
                func=create_project_structure,
                description="Create a project structure with appropriate folders and files",
            ),
            Tool(
                name="create_file",
                func=create_file,
                description="Create a file with the given content"
            ),
            Tool(
                name="create_directory",
                func=create_directory,
                description="Create a directory and its parent directories if they don't exist"
            ),
            Tool(
                name="generate_frontend_code",
                func=generate_frontend_code,
                description="Generate frontend code using the frontend agent"
            ),
            Tool(
                name="generate_backend_code",
                func=generate_backend_code,
                description="Generate backend code using the backend agent"
            ),
            Tool(
                name="generate_misc_code",
                func=generate_misc_code,
                description="Generate miscellaneous code using the misc agent"
            ),
            Tool(
                name="run_in_codesandbox",
                func=run_in_codesandbox,
                description="Run code in a CodeSandbox environment and return the results"
            )
        ]

class FrontendAgent:
    """A specialized agent for frontend development."""
    
    def __init__(self, temperature: float = 0.3):
        """Initialize the frontend agent.
        
        Args:
            temperature: The temperature for the LLM (0.0 to 1.0)
        """
        self.llm = self._create_llm(temperature)
    
    def _create_llm(self, temperature: float):
        """Create the LLM for the frontend agent."""
        from langchain_google_genai import ChatGoogleGenerativeAI
        import os
        from dotenv import load_dotenv
        
        load_dotenv()
        
        return ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",       
            temperature=temperature,
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )
    
    async def generate_code(self, prompt: str, framework: str = "react") -> str:
        """Generate frontend code based on the given prompt and framework."""
        try:
            from langchain_core.messages import HumanMessage

            full_prompt = f"Generate {framework} frontend code for: {prompt}. Include complete component code with proper imports, state management, and styling."
            response = await self.llm.ainvoke([HumanMessage(content=full_prompt)])
            return response.content
        except Exception as e:
            return f"Error generating frontend code: {str(e)}"

class BackendAgent:
    """A specialized agent for backend development."""
    
    def __init__(self, temperature: float = 0.3):
        """Initialize the backend agent.
        
        Args:
            temperature: The temperature for the LLM (0.0 to 1.0)
        """
        self.llm = self._create_llm(temperature)
    
    def _create_llm(self, temperature: float):
        """Create the LLM for the backend agent."""
        from langchain_google_genai import ChatGoogleGenerativeAI
        import os
        from dotenv import load_dotenv
        
        load_dotenv()
        
        return ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=temperature,
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )
    
    async def generate_code(self, prompt: str, framework: str = "express") -> str:
        """Generate backend code based on the given prompt and framework."""
        try:
            from langchain_core.messages import HumanMessage
            
            full_prompt = f"Generate {framework} backend code for: {prompt}. Include complete API endpoints, database models, controllers, and middleware with proper error handling and validation."
            response = await self.llm.ainvoke([HumanMessage(content=full_prompt)])
            return response.content
        except Exception as e:
            return f"Error generating backend code: {str(e)}"

class MiscAgent:
    """A specialized agent for miscellaneous coding tasks."""
    
    def __init__(self, temperature: float = 0.3):
        """Initialize the misc agent.
        
        Args:
            temperature: The temperature for the LLM (0.0 to 1.0)
        """
        self.llm = self._create_llm(temperature)
    
    def _create_llm(self, temperature: float):
        """Create the LLM for the misc agent."""
        from langchain_google_genai import ChatGoogleGenerativeAI
        import os
        from dotenv import load_dotenv
        
        load_dotenv()
        
        return ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=temperature,
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )
    
    async def generate_code(self, prompt: str) -> str:
        """Generate miscellaneous code based on the given prompt."""
        try:
            from langchain_core.messages import HumanMessage
            
            full_prompt = f"Generate code for: {prompt}. Include complete implementation with proper error handling, documentation, and examples."
            response = await self.llm.ainvoke([HumanMessage(content=full_prompt)])
            return response.content
        except Exception as e:
            return f"Error generating miscellaneous code: {str(e)}" 