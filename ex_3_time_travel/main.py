from langgraph.graph import StateGraph
from langgraph.checkpoint.memory import MemorySaver
from ex_3_time_travel.state import GraphState
from ex_3_time_travel.nodes import generate_text, run_subgraph, human_review

# -------------------------
# BUILD MAIN GRAPH
# -------------------------
def build_graph():
    graph = StateGraph(GraphState)

    graph.add_node("generate", generate_text)
    graph.add_node("subgraph", run_subgraph)
    graph.add_node("review", human_review)

    graph.set_entry_point("generate")

    graph.add_edge("generate", "subgraph")
    graph.add_edge("subgraph", "review")

    return graph.compile(checkpointer=MemorySaver(), interrupt_before=["review"])


# -------------------------
# RUN WORKFLOW
# -------------------------
if __name__ == "__main__":
    # -------------------------
    # TIME TRAVEL DEMO
    # -------------------------

    app = build_graph()

    config = {"configurable": {"thread_id": "thread-1"}}

    print("\n=== RUN 1: Initial run (pauses before review) ===")
    app.invoke({"text": ""}, config=config)
    print("[Paused before review node]")

    print("\n=== RUN 1 (continued): Resume for human review ===")
    app.invoke(None, config=config)

    print("\n=== RUN 2: TIME TRAVEL (Start from subgraph) ===")

    # Find the checkpoint where "subgraph" is the next node to run
    history = list(app.get_state_history(config))
    target = next(s for s in history if s.next == ("subgraph",))

    # Modify state at the checkpoint before replaying
    updated_config = app.update_state(target.config, {"text": "Overridden before subgraph."})

    # Replay from the updated checkpoint — pauses before review
    app.invoke(None, config=updated_config)
    print("[Paused before review node]")

    print("\n=== RUN 2 (continued): Resume for human review ===")
    result = app.invoke(None, config=config)

    print("\nFinal output after time travel + human review:")
    print(result["text"])