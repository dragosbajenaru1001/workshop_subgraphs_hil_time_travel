from langgraph.graph import StateGraph
from ex_2_human_in_the_loop.state import GraphState


# -------------------------
# SUBGRAPH NODE
# -------------------------
def improve_text(state: GraphState):
    print("[Subgraph] Improving text...")
    state["text"] += " It has been enhanced by subgraph."
    return state


# -------------------------
# BUILD SUBGRAPH
# -------------------------
def build_subgraph():
    graph = StateGraph(GraphState)

    graph.add_node("improve", improve_text)
    graph.set_entry_point("improve")

    return graph.compile()
