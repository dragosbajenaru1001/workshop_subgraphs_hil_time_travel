from ex_1_subgraphs.state import GraphState
from ex_1_subgraphs.subgraph import build_subgraph

# Initialize subgraph
subgraph_app = build_subgraph()


# -------------------------
# NODE 1: GENERATE TEXT
# -------------------------
def generate_text(state: GraphState):
    print("\n[Node] Generating text...")
    state["text"] = "This is AI generated content."
    return state


# -------------------------
# NODE 2: CALL SUBGRAPH
# -------------------------
def run_subgraph(state: GraphState):
    print("\n[Node] Running subgraph...")
    return subgraph_app.invoke(state)


# -------------------------
# NODE 3: FORMAT OUTPUT
# -------------------------
def format_output(state: GraphState):
    print("\n[Node] Formatting output...")
    state["text"] = f"[FINAL] {state['text']}"
    return state
