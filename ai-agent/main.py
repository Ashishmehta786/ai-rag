from dotenv import load_dotenv
load_dotenv()

from langchain_core.messages import HumanMessage
from fastapi import FastAPI, UploadFile, File, Request
from pydantic import BaseModel
from langchain.memory import ConversationBufferMemory
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
from agent.llm import llm
import os
from db.vectorstore import vector_store
from rich.console import Console


from rich.markdown import Markdown

from langchain_text_splitters import RecursiveCharacterTextSplitter
from loaders.loaders import text_loader
from agent.multi_agent import MultiAgentSystem
from agent.web_tools import WebTools
import asyncio
from dotenv import load_dotenv
load_dotenv()
from agent.llm import llm
from agent.single_coding_agent import SingleCodingAgent

app = FastAPI()
console = Console()

# Initialize the multi-agent system
multi_agent = MultiAgentSystem()
web_tools = WebTools()

class QueryRequest(BaseModel):
    query: str
    agent_type: str = "coding"

class ApiDocsRequest(BaseModel):
    query: str
    api_url: str

class ExtractCodeRequest(BaseModel):
    url: str
    
miniagent=SingleCodingAgent()

print("user agent", os.getenv("USER_AGENT"))

@app.get("/")
async def root():
    return {"message": "Server is working fine"}


UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload")
async def upload_file(request: Request):
    form = await request.form()
    for key, value in form.items():
        print(f"Field: {key}, Type: {type(value)}")

        # Check if it's a file
        if hasattr(value, "read") and hasattr(value, "filename"):
            print("✔️ Detected file field.")

            contents = await value.read()

            # Save to disk
            save_path = os.path.join(UPLOAD_DIR, value.filename)
            with open(save_path, "wb") as f:
                f.write(contents)

            print(f"📁 File saved to {save_path}")
        else:
            print(f"📝 Not a file field: {key} = {value}")

    return {"message": "File(s) uploaded and saved successfully"}

@app.post("/query")
async def process_query(request:Request):
    try:
        query =  request.query_params["query"]
        agent_type = request.query_params.get("agent_type", "coding")
        response = await multi_agent.route_request(
            query,
            agent_type
        )
        return {
            "response": response["response"],
            "thought_process": response["thought_process"]
        }
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        return {"error": str(e)}

@app.post("/search-api-docs")
async def search_api_docs(request: ApiDocsRequest):
    try:
        result = await web_tools.search_api_docs(request.query, request.api_url)
        md=Markdown(result)
        console.print(md)

        return {"result": result}
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        return {"error": str(e)}

@app.post("/extract-code")
async def extract_code(request: ExtractCodeRequest):
    try:
        result = await web_tools.extract_code_examples(request.url)
        return {"result": result}
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        return {"error": str(e)}

@app.post("/ask")
async def askAgent(req: Request):
    try:
        question = "Build a blog layout with Header, PostCard, Footer components."
        response = miniagent.ask(question)  # response is a string
        return {"response": response}
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        return {"error": str(e)}

# Initialize vector store with uploaded documents
@app.on_event("startup")
async def startup_event():
    docs = text_loader("./uploaded_files/main.txt")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=80)
    all_splits = text_splitter.split_documents(docs)
    texts = [doc.page_content for doc in all_splits]
    _ = vector_store.add_texts(texts, metadatas=[doc.metadata for doc in all_splits])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

