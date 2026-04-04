from ex_3_time_travel.state import GraphState
from ex_3_time_travel.subgraph import build_subgraph

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
# NODE 3: HUMAN-IN-LOOP
# -------------------------
def human_review(state: GraphState):
    print("\n[Node] Human Review")
    print("Current Output:", state["text"])

    decision = input("Approve or edit? (yes/edit): ")

    if decision.lower() == "edit":
        new_text = input("Enter updated text: ")
        state["text"] = new_text

    return state