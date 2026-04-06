# TODO: Articol de Presa cu Human Review si Time Travel

**Timp estimat: 25 minute**

## Arhitectura

```
[draft] → [subgraph: refine] → [review]
                                   ↑
                              omul aproba
                              sau rescrie
                                   ↓
                       TIME TRAVEL: revino la
                       subgraph cu text modificat
```

---

## TODO 1 — `state.py`
Inlocuieste campul `text: str` cu campurile necesare in `SharedState`:
- `article` — articolul generat (string)
- `approved` — boolean care indica daca omul a aprobat articolul

---

## TODO 2 — `nodes.py` — nodul `agent_write_article`
Inlocuieste `draft_text` cu un nod care apeleaza Groq pentru a genera un articol de presa scurt.

System prompt: `Esti un jurnalist. Scrie un articol de presa scurt (3-5 propozitii) despre un eveniment fictiv. Returneaza doar articolul, fara titlu sau explicatii.`
User prompt: `Scrie un articol de presa.`
```python
from groq import Groq

client = Groq()

def agent_write_article(state: SharedState):
    print("\n[Node] Agent Write Article (Groq)...")

    response = #ToDo

    state["article"] = response.choices[0].message.content
    print("\n[Agent] Articol generat:\n", state["article"])
    return state
```

---

## TODO 3 — `subgraph.py` — nodul `editor_final`
Inlocuieste `subgraph_text` cu un nod `editor_final` care:
- Primeste `state["article"]`
- Adauga un header de presa deasupra articolului:
  ```
  === ARTICOL DE PRESA ===
  <articolul>
  ========================
  ```
- Returneaza state-ul actualizat

---

## TODO 4 — `nodes.py` — nodul `human_review`
Actualizeaza `human_review` astfel incat sa afiseze articolul si sa astepte decizia omului:
- Daca raspunsul este `"edit"`, citeste articolul nou pastat (multi-line, terminat cu `###`)
- Seteaza `state["approved"] = True` in ambele cazuri

```python
def human_review(state: SharedState):
    print("\n[Review] Articol curent:\n", state["article"])
    decizie = input("\nAproba sau editeaza? (yes/edit): ")

    if decizie.lower() == "edit":
        print("Lipeste articolul nou, apoi scrie '###' pe o linie separata si apasa Enter:")
        lines = []
        while True:
            line = input()
            if line.strip() == "###":
                break
            lines.append(line)
        state["article"] = "\n".join(lines)

    state["approved"] = True
    return state
```

---

## TODO 5 — `main.py`
Actualizeaza graful principal:
- Redenumeste nodul `"draft"` in `"agent_write_article"` si inlocuieste importul `draft_text` cu `agent_write_article`
- Redenumeste nodul `"review"` in `"human_review"` si actualizeaza `interrupt_before=["human_review"]`
- Actualizeaza invoke-ul initial cu campurile noi:

```python
app.invoke({"article": "", "approved": False}, config=config)
```

- Actualizeaza time travel sa modifice `"article"` in loc de `"text"`:

```python
updated_config = app.update_state(target.config, {"article": "Articol modificat prin time travel."})
```

- Actualizeaza output-ul final:

```python
print("\nArticol final dupa time travel + human review:")
print(result["article"])
print("Aprobat:", result["approved"])
```

---

## TODO 6 — `main.py` — Time travel pana la nodul `agent_write_article`
Adauga un al treilea bloc de time travel care reporneste fluxul de la inceput, inainte de generarea articolului.

- Gaseste checkpoint-ul cu `next == ("agent_write_article",)` din istoric
- Nu modifica state-ul — calatoreste la checkpoint-ul respectiv fara `update_state`
- Ruleaza graful de la acel checkpoint (va genera un articol nou, va trece prin `editor_final`, si se va opri inainte de `human_review`)
- Reia si review-ul final

```python
print("\n=== RUN 3: TIME TRAVEL (Start from agent_write_article) ===")

history = list(app.get_state_history(config))
target_draft = next(s for s in history if s.next == ("agent_write_article",))

# Replay de la inceput, fara modificarea state-ului
app.invoke(None, config=target_draft.config)
print("[Paused before review node]")

print("\n=== RUN 3 (continued): Resume for human review ===")
result3 = app.invoke(None, config=config)

print("\nArticol final dupa time travel la draft:")
print(result3["article"])
```

> **Observatie:** De fiecare data cand repornesti de la `agent_write_article`, Groq genereaza un articol diferit — time travel nu "memoreaza" output-ul LLM-ului, ci reia executia de la acel punct.

---

## Testare

- [ ] Ruleaza si alege `yes` — verifica ca textul generat apare formatat in output final
- [ ] Ruleaza din nou si alege `edit` — verifica ca articolul editat de om (multi-line) este folosit in output final
- [ ] Verifica time travel — articolul modificat la checkpoint trece din nou prin `editor_final` inainte de review

---

## Rulare
```bash
python -m ex_3_time_travel.main
```
