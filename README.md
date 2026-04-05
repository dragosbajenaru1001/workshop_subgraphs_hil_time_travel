# LangGraph: Subgraphs + Human-in-the-Loop + Time Travel

Three separate, runnable examples that each demonstrate one core LangGraph feature.
Each example builds on the previous one — read them in order if you're new to LangGraph.

---

## What is LangGraph?

LangGraph is a library for building AI workflows as **graphs** — think of it as a flowchart where each box is a step your AI takes, and arrows connect the steps in order.

Every example here uses the same simple idea: pass a piece of text through a series of steps, transforming it along the way.

---

## Setup

```bash
pip install -r requirements.txt
```

---

## The shared building block

Every example passes one value through the graph — a piece of text:

```python
class SharedState(TypedDict):
    text: str
```

Think of `SharedState` as a backpack that gets handed from step to step. Each step can read from it or add something to it.

---

## Example 1 — Subgraphs (`ex_1_subgraphs`)

**The concept:** A graph inside a graph.

Sometimes a step in your workflow is complex enough to deserve its own mini-graph. Instead of cramming everything into one big graph, you break it out into a **subgraph** — a separate, self-contained graph that the main graph calls like any other step.

**Flow:**

```
draft → subgraph → final
```

| Step | What happens |
|------|--------------|
| `draft` | Creates the initial text: `"The quick brown fox jumps over the lazy dog."` |
| `subgraph` | Hands the text to a mini-graph that refines it by appending `" (refined by subgraph)"` |
| `final` | Wraps the final text with a `[FINAL]` label |

**Why use subgraphs?**
- Keeps complex logic self-contained and reusable
- The main graph doesn't need to know what happens inside the subgraph
- You can swap out the subgraph without touching the rest of the flow

```bash
python -m ex_1_subgraphs.main
```

**Expected output:**
```
=== RUN: SUBGRAPHS DEMO ===

[Node] Drafting initial text...

[Node] Refining text via subgraph...
[Subgraph] Adding text from subgraph...

[Node] Preparing final output...

Final Output:
[FINAL] The quick brown fox jumps over the lazy dog. (refined by subgraph)
```

---

## Example 2 — Human-in-the-Loop (`ex_2_human_in_the_loop`)

**The concept:** Pause the AI and ask a real person for input.

Not every AI decision should be fully automated. Human-in-the-loop lets you **interrupt** the graph mid-run, show the current output to a person, and let them approve or correct it before the graph continues.

This example uses `MemorySaver` (checkpointing) and `interrupt_before` to pause execution automatically before the review step, then resume it in a second invoke call.

**Flow:**

```
draft → subgraph → [pause] → review
```

| Step | What happens |
|------|--------------|
| `draft` | Creates the initial text |
| `subgraph` | Refines the text (same mini-graph as Example 1) |
| `[pause]` | Graph stops automatically — state is saved to a checkpoint |
| `review` | **Resumes and asks you:** approve as-is, or type new text |

**Why use human-in-the-loop?**
- Catches mistakes before they propagate further in the workflow
- Lets humans stay in control of important decisions
- Useful for content moderation, approvals, or anywhere accuracy matters

```bash
python -m ex_2_human_in_the_loop.main
```

**What you'll see:**
```
=== RUN 1: Draft text (pause before review) ===

[Node] Drafting initial text...

[Node] Refining text via subgraph...
[Subgraph] Adding text from subgraph...
[Paused before review node]

=== RUN 1 (continued): Resume for human review ===

[Node] Human Review
Current Output: The quick brown fox jumps over the lazy dog. (refined by subgraph)
Approve or edit? (yes/edit):
```

Type `yes` to approve, or `edit` to replace the text with something of your own.

---

## Example 3 — Time Travel (`ex_3_time_travel`)

**The concept:** Save every step, then go back in time and re-run from any point.

LangGraph can save a **checkpoint** (a snapshot of the state) after every step. This means you can look back at the full history of a run, pick any earlier moment, change something, and replay the graph from there — like an undo button for your AI workflow.

**Flow:**

```
draft → subgraph → review   (paused here automatically)
```

The demo does four phases:

| Phase | What happens |
|-------|--------------|
| **Run 1** | Runs the graph normally, pauses automatically before `review` |
| **Run 1 (continued)** | Resumes from the pause and completes human review |
| **Run 2** | Goes back to the checkpoint just before `subgraph`, overrides the text, then replays — pauses before `review` again |
| **Run 2 (continued)** | Resumes from the pause and completes human review with the time-travelled state |

**Why use time travel?**
- Debug a failed run by replaying it with a fix
- Test "what if" scenarios by branching from an earlier state
- Recover from a bad AI output without starting over from scratch

```bash
python -m ex_3_time_travel.main
```

**Expected output:**
```
=== RUN 1: Initial run (pauses before review) ===

[Node] Drafting initial text...

[Node] Refining text via subgraph...
[Subgraph] Adding text from subgraph...
[Paused before review node]

=== RUN 1 (continued): Resume for human review ===

[Node] Human Review
Current Output: The quick brown fox jumps over the lazy dog. (refined by subgraph)
Approve or edit? (yes/edit):

=== RUN 2: TIME TRAVEL (Start from subgraph) ===

[Node] Refining text via subgraph...
[Subgraph] Adding text from subgraph...
[Paused before review node]

=== RUN 2 (continued): Resume for human review ===

[Node] Human Review
Current Output: Overridden before subgraph. (refined by subgraph)
Approve or edit? (yes/edit):

Final output after time travel + human review:
Overridden before subgraph. (refined by subgraph)
```

Notice that in Run 2, `draft` is **skipped** — the graph jumped straight to `subgraph` using the saved checkpoint, with the overridden text injected at that point. Both runs complete the full human review step before finishing.

---

## How the examples relate to each other

```
Example 1 (Subgraphs)
  └── Example 2 (Human-in-the-Loop) — adds checkpointing and a human review step
        └── Example 3 (Time Travel) — adds state history inspection and replay
```

Each example adds one new capability on top of the same core graph structure.

---

## Project structure

```
ex_1_subgraphs/
  state.py       — defines SharedState (the shared backpack)
  subgraph.py    — the mini-graph that refines text
  nodes.py       — the individual steps (draft_text, run_subgraph, final_output)
  main.py        — builds and runs the full graph

ex_2_human_in_the_loop/
  state.py
  subgraph.py
  nodes.py       — same as ex_1, but human_review step replaces final_output
  main.py

ex_3_time_travel/
  state.py
  subgraph.py
  nodes.py
  main.py        — runs twice: normal run, then time-travel fork from a past checkpoint
```
