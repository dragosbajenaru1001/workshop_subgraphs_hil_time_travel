# TODO: Code Review cu Generare prin Agent Groq si Aprobare Umana

**Timp estimat: 20 minute**

## Arhitectura

```
[agent_generate] → [subgraph] → [human_review] → output final
                                      ↑
                                 omul aproba
                                 sau editeaza codul
```

---

## TODO 1 — `state.py`
`SharedState` contine deja campul `text: str`. Adauga campul lipsa:
- `approved` — boolean care indica daca omul a aprobat codul

---

## TODO 2 — `nodes.py` — nodul `agent_generate`
Inlocuieste `draft_text` cu un nod `agent_generate` care apeleaza Groq pentru a genera cod Python.

```python
from groq import Groq

client = Groq()

def agent_generate(state: SharedState):
    print("\n[Node] Agent Generate (Groq)...")

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "Esti un programator Python. Scrie o functie Python simpla si utila. Returneaza doar codul, fara explicatii.",
            },
            {
                "role": "user",
                "content": "Scrie o functie Python.",
            },
        ],
    )

    state["text"] = response.choices[0].message.content
    print("\n[Agent] Cod generat:\n", state["text"])
    return state
```

---

## TODO 3 — `nodes.py` — nodul `human_review`
Actualizeaza nodul `human_review` existent astfel incat sa afiseze codul generat si sa astepte decizia omului prin `input()`:
- Daca raspunsul este `"edit"`, cere codul nou si actualizeaza `state["text"]`
- Seteaza `state["approved"] = True` in ambele cazuri

```python
def human_review(state: SharedState):
    print("\n[Review] Cod curent:\n", state["text"])
    decizie = input("\nAproba sau editeaza? (yes/edit): ")

    if decizie.lower() == "edit":
        print("Lipeste codul nou, apoi scrie '###' pe o linie separata si apasa Enter:")
        lines = []
        while True:
            line = input()
            if line.strip() == "###":
                break
            lines.append(line)
        state["text"] = "\n".join(lines)

    state["approved"] = True
    return state
```

---

## TODO 4 — `subgraph.py`
Inlocuieste nodul `subgraph_text` (care adauga `"(refined by subgraph)"`) cu un nod `process` care:
- Primeste `state["text"]`
- Adauga un comentariu de header deasupra codului (ex: `"# Generat de AI\n" + text`)
- Returneaza state-ul actualizat

---

## TODO 5 — `main.py`
Actualizeaza graful principal (inlocuieste nodul `draft` cu `agent_generate` si redenumeste importul):

```
agent_generate → subgraph → human_review
```

Schimba:
```python
# inainte (schelet)
graph.add_node("draft", draft_text)
from ex_2_human_in_the_loop.nodes import draft_text, run_subgraph, human_review

# dupa
graph.add_node("agent_generate", agent_generate)
from ex_2_human_in_the_loop.nodes import agent_generate, run_subgraph, human_review
```

Actualizeaza si invoke-ul initial:
```python
app.invoke({"text": "", "approved": False}, config=config)

result = app.invoke(None, config=config)
print("\nOutput final:\n", result["text"])
print("Aprobat:", result["approved"])
```

---

## Testare

- [ ] Ruleaza si alege `yes` — verifica ca codul generat de Groq apare in output final
- [ ] Ruleaza din nou si alege `edit` — verifica ca codul editat de om este folosit in output final

---

## Rulare
```bash
python -m ex_2_human_in_the_loop.main
```
