from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
load_dotenv(dotenv_path="../.env", override=True, encoding="utf-8")

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=1, max_output_tokens=512,
                             api_key=os.getenv("GOOGLE_API_KEY"))


