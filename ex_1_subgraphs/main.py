from dotenv import load_dotenv
load_dotenv()

from langgraph.graph import StateGraph
from ex_1_subgraphs.state import GraphState
from ex_1_subgraphs.nodes import generate_text, run_subgraph, format_output


# -------------------------
# BUILD MAIN GRAPH
# -------------------------
def build_graph():
    graph = StateGraph(GraphState)

    graph.add_node("generate", generate_text)
    graph.add_node("subgraph", run_subgraph)
    graph.add_node("format", format_output)

    graph.set_entry_point("generate")

    graph.add_edge("generate", "subgraph")
    graph.add_edge("subgraph", "format")

    return graph.compile()


# -------------------------
# RUN WORKFLOW
# -------------------------
if __name__ == "__main__":
    app = build_graph()

    print("\n=== RUN: SUBGRAPHS DEMO ===")
    result = app.invoke({"text": ""})

    print("\nFinal Output:")
    print(result["text"])
