from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent

from tools import ALL_TOOLS
from agent.prompts import SYSTEM_PROMPT
from config import GROQ_API_KEY, LLM_MODEL


def build_agent():
    llm = ChatGroq(
        model=LLM_MODEL,
        api_key=GROQ_API_KEY,
        temperature=0.1
    )

    agent = create_react_agent(
        model=llm,
        tools=ALL_TOOLS,
        prompt=SYSTEM_PROMPT
    )

    return agent