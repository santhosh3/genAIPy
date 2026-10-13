from dotenv import load_dotenv

load_dotenv()

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
# from tavily import TavilyClient
from langchain_tavily import TavilySearch

# tavily = TavilyClient()

# @tool
# def search(query: str) -> str:
#     """
#     Tool to search over internet
#     Args:
#         query: The query to search for
#     Returns:
#         The search result
#     """
#     print(f"Searching for {query}")
#     return tavily.search(query=query)
    


llm = ChatGoogleGenerativeAI(model="gemini-3.6-flash")
tools = [TavilySearch()]
agent = create_agent(model=llm, tools=tools)


def main():
   result = agent.invoke(
        {
            "messages": [
                HumanMessage(
                    content="What is the weather in Wanaparthy?"
                )
            ]
        }
    )

   print(result)

if __name__ == "__main__":
    main()
