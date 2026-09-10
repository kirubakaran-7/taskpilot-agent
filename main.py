"""TaskPilot - a small agentic assistant you talk to in the terminal.

Run:  python main.py
It keeps chat history so it remembers context, and prints its tool calls so you
can see it think.
"""
from langchain_core.messages import AIMessage, HumanMessage

from agent.core import build_agent

BANNER = r"""
 _____         _    ____  _ _       _
|_   _|_ _ ___| | _|  _ \(_) | ___ | |_
  | |/ _` / __| |/ / |_) | | |/ _ \| __|
  | | (_| \__ \   <|  __/| | | (_) | |_
  |_|\__,_|___/_|\_\_|   |_|_|\___/ \__|

TaskPilot - agentic AI assistant
Type a task. Commands: 'exit' to quit, 'reset' to clear memory.
"""


def main():
    print(BANNER)
    agent = build_agent(verbose=True)
    chat_history = []

    while True:
        try:
            user_input = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            break

        if not user_input:
            continue
        if user_input.lower() in {"exit", "quit"}:
            print("Bye!")
            break
        if user_input.lower() == "reset":
            chat_history = []
            print("(memory cleared)")
            continue

        try:
            result = agent.invoke({"input": user_input, "chat_history": chat_history})
            answer = result["output"]
        except Exception as exc:
            answer = f"Something went wrong: {exc}"

        print(f"\nTaskPilot: {answer}")
        chat_history.append(HumanMessage(content=user_input))
        chat_history.append(AIMessage(content=answer))


if __name__ == "__main__":
    main()
