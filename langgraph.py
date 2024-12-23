from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated, Sequence
import operator

# Define the State for the Chat Architecture
class ChatState(TypedDict):
    session_id: str
    chat_history: Annotated[list[dict], operator.add]
    context: dict
    query: str
    response: str


# Node Definitions

# Session Manager Node
def session_manager(state: ChatState):
    """Manages session ID and metadata."""
    state['session_id'] = "unique_session_id"
    return state


# Chat History Manager Node
def chat_history_manager(state: ChatState):
    """Stores and retrieves chat history."""
    state['chat_history'].append({"query": state['query'], "response": state.get('response', '')})
    return state


# Context Augmentation Node
def context_augmentation(state: ChatState):
    """Augments the query with historical context."""
    state['context'] = {"augmented_query": f"Augmented: {state['query']} with history"}
    return state


# Agent Orchestration Node
def agent_orchestration(state: ChatState):
    """Orchestrates agents to ensure unified context."""
    state['context']['orchestration_status'] = "Agents orchestrated"
    return state


# Follow-Up Handling Node
def follow_up_handler(state: ChatState):
    """Handles follow-up queries."""
    state['response'] = f"Processed follow-up for query: {state['query']}"
    return state


# Define the Graph Workflow
workflow = StateGraph(ChatState)

# Add Nodes
workflow.add_node("session_manager", session_manager)
workflow.add_node("chat_history_manager", chat_history_manager)
workflow.add_node("context_augmentation", context_augmentation)
workflow.add_node("agent_orchestration", agent_orchestration)
workflow.add_node("follow_up_handler", follow_up_handler)

# Define Edges
workflow.set_entry_point("session_manager")
workflow.add_edge("session_manager", "chat_history_manager")
workflow.add_edge("chat_history_manager", "context_augmentation")
workflow.add_edge("context_augmentation", "agent_orchestration")
workflow.add_edge("agent_orchestration", "follow_up_handler")
workflow.add_edge("follow_up_handler", END)

# Compile the Workflow
app = workflow.compile()

# Test the Graph
input_state = {
    "session_id": "",
    "chat_history": [],
    "context": {},
    "query": "What was my last query?",
    "response": ""
}

output_state = app.invoke(input_state)
print(output_state)
