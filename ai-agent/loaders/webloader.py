from langchain_community.document_loaders import WebBaseLoader
from langchain.schema import Document
from bs4 import BeautifulSoup
from agent.llm import llm

web_loader = WebBaseLoader(llm=llm, url="https://google.com")


def WEBloader(url):
    return web_loader.load()
