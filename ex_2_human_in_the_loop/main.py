from langgraph.graph import StateGraph
from ex_2_human_in_the_loop.state import GraphState
from ex_2_human_in_the_loop.nodes import generate_text, run_subgraph, human_review

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

    return graph.compile()


# -------------------------
# RUN WORKFLOW
# -------------------------
if __name__ == "__main__":
    app = build_graph()

    print("\n=== RUN: HUMAN-IN-THE-LOOP EXECUTION ===")
    result = app.invoke({"text": ""})

    print("\nFinal Output:")
    print(result["text"])