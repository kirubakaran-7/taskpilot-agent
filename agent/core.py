"""Wire up the agent: an LLM + the tools + a prompt, run by an AgentExecutor."""
import os

from dotenv import load_dotenv
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from .tools import ALL_TOOLS

load_dotenv()

SYSTEM_PROMPT = (
    "You are TaskPilot, an AI assistant that completes multi-step tasks. "
    "Think step by step and use the tools when they help. Use the calculator for "
    "math, web_search for current facts, and the notes tools to remember things. "
    "When you have enough information, give a clear final answer."
)


def _build_llm():
    backend = os.getenv("BACKEND", "openai").lower()
    if backend == "openai":
        from langchain_openai import ChatOpenAI

        return ChatOpenAI(
            model=os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini"),
            temperature=0.0,
        )
    if backend == "ollama":
        from langchain_ollama import ChatOllama

        return ChatOllama(
            model=os.getenv("OLLAMA_CHAT_MODEL", "llama3.1"),
            temperature=0.0,
        )
    raise ValueError(f"Unknown BACKEND: {backend} (use 'openai' or 'ollama').")


def build_agent(verbose=True):
    llm = _build_llm()
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder("agent_scratchpad"),
        ]
    )
    agent = create_tool_calling_agent(llm, ALL_TOOLS, prompt)
    return AgentExecutor(
        agent=agent,
        tools=ALL_TOOLS,
        verbose=verbose,
        handle_parsing_errors=True,
        max_iterations=8,
    )
