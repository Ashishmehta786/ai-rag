from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
from langchain_core.tools import Tool
from langchain.agents import initialize_agent, AgentType
from langchain_community.utilities import GoogleSearchAPIWrapper
import os
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

search_apikey = os.getenv("GOOGLE_SEARCH_API_KEY")
search_cseid = os.getenv("GOOGLE_CSE_ID")

class SingleCodingAgent:
    def __init__(self):
        self.search = GoogleSearchAPIWrapper(
            google_api_key=search_apikey,
            google_cse_id=search_cseid
        )
        self.llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)
        self.promptTemplate = ChatPromptTemplate.from_messages([
            ("system", "You are a coding assistant that builds fullstack projects. Use tools when needed."),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])
        self.tools = self.get_tools()
        self.agent = initialize_agent(
            tools=self.tools,
            llm=self.llm,
            prompt=self.promptTemplate,
            agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
            handle_parsing_errors=True,
        )
    def create_folder_graph(self)->dict:
        """ Creates a folder graph in form of dictionary for a Next.js app."""
        folder_structure = {
            "code": {
                "components": {},
                "pages": {},
                "public": {},
                "styles": {},
                "utils": {}
            }
        }
        return folder_structure

    def create_folder_structure(self, code_files: dict) -> dict:
        """Create a general folder structure inside a 'code' directory for a Next.js app and return example code files."""
        base_dir = os.path.join(os.getcwd(), "code")
        
        for file_path in code_files:
            full_path = os.path.join(base_dir, os.path.relpath(file_path, 'code'))
            os.makedirs(os.path.dirname(full_path), exist_ok=True)

        return code_files

    def generate_component(self, component_spec: str) -> dict:
        """Dynamically generate a React/Next.js component and return its code as a dictionary."""
        component_name = component_spec.strip().split()[0].capitalize()
        code = (
            f"export default function {component_name}() {{\n"
            f"  return <div>This is the {component_name} component</div>;\n"
            f"}}"
        )
        return {f"code/components/{component_name}.tsx": code}
    
    def generate_code(self, code_spec: str) -> str:
        """Generate code based on a specification."""
        response = self.agent.run({"input": code_spec})
        return response

    def write_code(self, code_map) -> str:
        """Write multiple code files to appropriate paths."""
        import ast

        if isinstance(code_map, str):
            try:
                code_map = ast.literal_eval(code_map)
            except Exception as e:
                return f"Error parsing code map: {str(e)}"

        if not isinstance(code_map, dict):
            return "Error: code_map is not a dictionary."

        created_files = []
        for relative_path, code in code_map.items():
            try:
                full_path = os.path.join(os.getcwd(), relative_path)
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                with open(full_path, "w", encoding="utf-8") as f:
                    f.write(code)
                created_files.append(relative_path)
            except Exception as e:
                return f"Failed to write {relative_path}: {str(e)}"

        return f"Code written to {len(created_files)} files:\n" + "\n".join(created_files)
    
    def get_tools(self) -> list[Tool]:
        """Return the tools available to the agent."""
        return [
            Tool.from_function(
                func=self.create_folder_structure,
                name="create_folder_structure",
                description=(
                    "Use this tool to generate the folder and file structure for a Next.js or React project. Returns a dictionary mapping file paths to initial content, suitable for writing. Also at each time the code is changed the folder structure remains same only the files are updated and in the right path where they are saved.The folder structure is created inside a code directory in the current working directory."
                )
            ),
            Tool.from_function(
                func=self.generate_component,
                name="generate_component",
                description="Use this tool to dynamically generate a reusable component by name or specification but this shall be used at the creation of the a new component then the code is generated."
            ),
            Tool.from_function(
                func=self.write_code,
                name="write_code",
                description="Use this tool to write code files to the appropriate paths."
            ),
            Tool.from_function(
                func=self.create_folder_graph,
                name="create_folder_graph",
                description=(
                    "Use this tool to create a folder graph in form of dictionary for a Next.js app. Returns the folder structure as a dictionary."
                )
            )
           ,
            Tool.from_function(
                func=self.generate_code,
                name="generate_code",
                description=(
                    "Use this tool to generate code of nextjs in typescript build good components. Returns the generated code as a string."
                )
            ),
            Tool.from_function(
                func=self.search.run,
                name="search",
                description=(
                    "Use this tool to search the web for information. Returns the search results."
                )
            ),
        ]

    def ask(self, prompt: str) -> str:
        """Ask the agent a question."""
        return self.agent.run({"input": prompt})