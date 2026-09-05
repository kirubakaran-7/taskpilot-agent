"""The tools the agent can call. The docstrings tell the LLM when to use each one."""
import json
import os

from langchain_core.tools import tool

from .calc import safe_eval

NOTES_FILE = "notes.json"


@tool
def calculator(expression):
    """Do basic math, e.g. "12 * (3 + 4) / 2". Use this instead of doing math yourself."""
    try:
        return str(safe_eval(expression))
    except Exception as exc:
        return f"Error: could not evaluate '{expression}' ({exc})."


@tool
def web_search(query):
    """Search the web for current info. Input is a short search query."""
    try:
        from langchain_community.tools import DuckDuckGoSearchRun

        return DuckDuckGoSearchRun().run(query)
    except Exception as exc:
        return f"Error: web search failed ({exc})."


def _read_notes():
    if not os.path.exists(NOTES_FILE):
        return []
    try:
        with open(NOTES_FILE, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except (json.JSONDecodeError, OSError):
        return []


def _write_notes(notes):
    with open(NOTES_FILE, "w", encoding="utf-8") as fh:
        json.dump(notes, fh, indent=2)


@tool
def save_note(text):
    """Save a short note or reminder for the user."""
    notes = _read_notes()
    notes.append(text)
    _write_notes(notes)
    return f"Saved. You now have {len(notes)} note(s)."


@tool
def list_notes(_=""):
    """List all saved notes. Pass an empty string as input."""
    notes = _read_notes()
    if not notes:
        return "No notes saved yet."
    return "\n".join(f"{i}. {note}" for i, note in enumerate(notes, 1))


ALL_TOOLS = [calculator, web_search, save_note, list_notes]
