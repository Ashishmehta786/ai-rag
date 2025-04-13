from langchain_community.document_loaders.pdf import PyPDFLoader

from langchain_community.document_loaders import WebBaseLoader
from langchain.schema import Document
from bs4 import BeautifulSoup
from typing import List
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.document_loaders.json_loader import JSONLoader
from langchain_community.document_loaders.text import TextLoader
from langchain_community.document_loaders.telegram import  TelegramChatApiLoader
# from langchain_community.document_loaders.markdown import MarkdownLoader
from langchain_community.document_loaders.notion import NotionDirectoryLoader
import asyncio

TeleLoader=TelegramChatApiLoader()

async def telegram_loader(chat_entity: str, api_id: int, api_hash: str, username: str):
    """Load Telegram chat data and return its content."""
    TeleLoader.chat_entity = chat_entity
    TeleLoader.api_id = api_id
    TeleLoader.api_hash = api_hash
    TeleLoader.username = username
    documents = await TeleLoader.load()
    return documents


async def notion_loader(token:str, database_id:str):
    """Load Notion database and return its content."""
    loader = NotionDirectoryLoader(token, database_id)
    documents = await loader.load()
    return documents



def pdf_loader(file_path: str):
    """Load a PDF file and return its content."""
    loader = PyPDFLoader(file_path)
    documents =  loader.load()
    return documents

async def webloader(url:str):
    loader = WebBaseLoader(url)
    documents = await loader.load()
    return documents

async def  csv_loader(file_path: str):
    """Load a CSV file and return its content."""
    loader = CSVLoader(file_path)
    documents = await loader.load()
    return documents
    
async def json_loader(file_path: str):
    """Load a JSON file and return its content."""
    loader = JSONLoader(file_path)
    documents = await loader.load()
    return documents

def text_loader(file_path: str)->List[Document]:
    """Load a text file and return its content."""
    loader = TextLoader(file_path)
    documents = loader.load()
    return documents

async def load_documents(file_path: str, file_type: str):
    """Load documents from a file based on its type."""
    if file_type == "pdf":
        return await pdf_loader(file_path)
    elif file_type == "web":
        return await webloader(file_path)
    elif file_type == "csv":
        return await csv_loader(file_path)
    elif file_type == "json":
        return await json_loader(file_path)
    elif file_type == "text":
        return await text_loader(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_type}")
