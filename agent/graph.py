import os
import logging
from agent.state import AgentState
from tools.llm_factory import create_llm
from tools.blob_tools import move_file, list_files
from langgraph.graph import StateGraph, END
from config.settings import MAX_STEPS, CATEGORIES, LLM_PROVIDER, LLM_MODEL, LLM_TEMPERATURE

logger = logging.getLogger(__name__)

# Create LLM for this agent (can be configured per-agent via env vars)
categorizer_llm = create_llm(
    provider=os.getenv("CATEGORIZER_LLM_PROVIDER", LLM_PROVIDER),
    model=os.getenv("CATEGORIZER_LLM_MODEL", LLM_MODEL),
    temperature=float(os.getenv("CATEGORIZER_LLM_TEMPERATURE", LLM_TEMPERATURE))
)


def pick_file(state: AgentState):
    try:
        state.setdefault("step", 0)
        if "files" not in state or state["files"] is None:
            logger.info("Initializing files from blob storage")
            state["files"] = list_files()

        if not state["files"]:
            logger.info("No more files to process")
            state["current_file"] = None
            return state

        state["current_file"] = state["files"][0]
        return state
    except Exception as e:
        logger.error(f"Error picking file: {str(e)}")
        return {"current_file": None}

def decide_category(state: AgentState):
    try:
        file = state.get("current_file")

        if not file:
            logger.warning("No file to categorize")
            state["category"] = "Others"
            return state

        ext = file.split(".")[-1].lower()
        logger.info(f"Categorizing file: {file} (extension: {ext})")

        prompt = f"""
        You are a file organizer.

        File name: {file}
        Extension: {ext}

        Categories:
        {list(CATEGORIES.keys())}

        Return ONLY the best category name.
        """

        category = categorizer_llm.invoke(prompt).content.strip()
        logger.info(f"Category decided: {category} for file: {file}")

        state["category"] = category
        return state
    except Exception as e:
        logger.error(f"Error deciding category for {state.get('current_file')}: {str(e)}")
        return {"category": "Others"}


def move(state: AgentState):
    try:
        filename = state.get("current_file")
        category = state.get("category")

        if not filename:
            logger.warning("No file to move")
            return state

        logger.info(f"Moving file: {filename} to category: {category}")
        move_file(filename, category)

        # Remove processed file
        state["files"] = [f for f in state["files"] if f != filename]
        logger.info(f"Files remaining: {len(state['files'])}")

        return state
    except Exception as e:
        logger.error(f"Error moving file {state.get('current_file')}: {str(e)}")
        # On error, still remove from list to avoid infinite loop
        remaining = [f for f in state["files"] if f != state.get("current_file")]
        return {"files": remaining}



def observe(state: AgentState):
    try:
        state["step"] = state.get("step", 0) + 1
        logger.info(f"Step {state['step']} completed")

        if state["step"] >= MAX_STEPS:
            logger.warning(f"Max steps ({MAX_STEPS}) reached")

        return state
    except Exception as e:
        logger.error(f"Error in observe: {str(e)}")
        return {"step": state.get("step", 0) + 1}



# Nodes imported above

graph = StateGraph(AgentState)

graph.add_node("pick_file", pick_file)
graph.add_node("decide_category", decide_category)
graph.add_node("move", move)
graph.add_node("observe", observe)

graph.set_entry_point("pick_file")

graph.add_edge("pick_file", "decide_category")
graph.add_edge("decide_category", "move")
graph.add_edge("move", "observe")

graph.add_conditional_edges(
    "observe",
    lambda s: END if not s.get("files") or s.get("step", 0) >= MAX_STEPS else "pick_file"
)

agent = graph.compile()
