import os
from dotenv import load_dotenv

from langchain.agents import load_tools, initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI  # or use OpenAI() if you're not using chat models
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.utilities import GoogleSearchAPIWrapper
from langchain_core.tools import Tool
load_dotenv()
llm=ChatGoogleGenerativeAI(temperature=0.5, model="gemini-1.5-flash", max_tokens=1000,api_key=os.getenv("GOOGLE_API_KEY"))

import requests
from langchain_core.tools import Tool

def manual_google_search(query: str) -> str:
    params = {
        "key": os.getenv("GOOGLE_SEARCH_API_KEY"),
        "cx": os.getenv("GOOGLE_CSE_ID"),
        "q": query
    }
    res = requests.get("https://www.googleapis.com/customsearch/v1", params=params, timeout=15)
    if res.status_code == 200:
        results = res.json()
        if "items" in results:
            return "\n".join([item["title"] + ": " + item["link"] for item in results["items"]])
        else:
            return "No results found."
    else:
        return f"Error {res.status_code}: {res.text}"

# Get env vars
search_apikey = os.getenv("GOOGLE_SEARCH_API_KEY")
search_cseid = os.getenv("GOOGLE_CSE_ID")

search = GoogleSearchAPIWrapper(
    google_api_key=search_apikey,
    google_cse_id=search_cseid,
)
# google_search_tool = Tool.from_function(
#     func=search.run,
#     name="google_search",
#     description="Search Google for recent information."
# )

print("running",manual_google_search("president of the USA"))
# print(search.run("who is the president of the USA?"))
# print(manual_google_search("current weather in Paris"))

# Use this as a LangChain tool
# google_search_tool = Tool.from_function(
#     func=manual_google_search,
#     name="google_search",
#     description="Search Google for recent information."
# )


# def get_weather_with_google(city: str) -> str:
#     query = f"current weather in {city}"
#     results = search.run(query)
#     return results  

# weather_tool = Tool.from_function(
#     func=get_weather_with_google,
#     name="get_weather",
#     description="Get the current weather of a given city using Google Search  and you can use tools for converting the fahrenheit to celsius. "
# )

# def fahrenheit_to_celsius(fahrenheit: str) -> float:
#         f = float(fahrenheit)
#         celsius = (f - 32) * 5 / 9
#         return round(celsius, 2)


# fahrenheit_to_celsius_tool = Tool.from_function(
#     func=fahrenheit_to_celsius,
#     name="fahrenheit_to_celsius",
#     description="Convert fahrenheit to celcuis."
# )

# tools = [google_search_tool]


# agent = initialize_agent(
#     tools=tools,
#     llm=llm,
#     agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
#     verbose=True,
# )

# result = agent.run("What is the capital of France and what's the temperature right now there in celcius?")
# print(result)
