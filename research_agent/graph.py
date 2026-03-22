from typing import TypedDict, Annotated
from operator import add
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from state import ResearchState


def route_from_supervisor(state: ResearchState) -> str:
    """
    This function is called by LangGraph after every supervisor run.
    It reads state["next_step"] and returns the NAME of the next node
    as a plain string. LangGraph uses that string to find the next node.
    """
    step = state.get("next_step", "search")

    routing = {
        "search": "searcher",
        "analyze": "analyst",
        "write": "writer",
        "done": END,
    }

    return routing.get(step, END)


def build_graph():
    from agents import supervisor_node, searcher_node, analyst_node, writer_node

    builder = StateGraph(ResearchState)

    builder.add_node("supervisor", supervisor_node)
    builder.add_node("searcher", searcher_node)
    builder.add_node("analyst", analyst_node)
    builder.add_node("writer", writer_node)

    builder.add_edge(START, "supervisor")
    builder.add_edge("searcher", "supervisor")
    builder.add_edge("analyst", "supervisor")
    builder.add_edge("writer", "supervisor")

    builder.add_conditional_edges(
        "supervisor",
        route_from_supervisor,
        {"searcher": "searcher", "analyst": "analyst", "writer": "writer", END: END},
    )

    checkpointer = MemorySaver()
    return builder.compile(checkpointer=checkpointer)


graph = build_graph()

if __name__ == "__main__":
    config = {"configurable": {"thread_id": "test-1"}}
    result = graph.invoke(
        {
            "topic": "fusion energy",
            "search_results": [],
            "ranked_results": [],
            "report": "",
            "next_step": "",
        },
        config=config,
    )
    print("Graph finished. next_step =", result["next_step"])
