# TODO: Sales Campaign cu Groq + 2 Subgrafuri

## Arhitectura

```
[load_lead] → [qualify_subgraph] → [pitch_subgraph] → [format_output]
```

- **Subgraf 1** — agent Groq califica lead-ul: HOT / WARM / COLD
- **Subgraf 2** — agent Groq genereaza un pitch de vanzari personalizat

---

## TODO 1 — `state.py`
Adauga campurile necesare in `GraphState`:
- `lead_name`, `company`, `industry`, `budget`
- `qualification` (HOT/WARM/COLD), `qualification_reason`
- `pitch`

---

## TODO 2 — `subgraph_qualify.py` *(fisier nou)*
Creeaza un subgraf cu un singur nod `analyze_lead` care:
- Apeleaza Groq cu datele lead-ului din state
- Completeaza `qualification` si `qualification_reason`

```python
from groq import Groq
client = Groq()  # citeste GROQ_API_KEY din environment
```

System prompt sugestie: *"Esti un agent de calificare vanzari. Analizeaza datele prospectului si raspunde cu: CALIFICARE: HOT/WARM/COLD. MOTIV: <scurt>"*

---

## TODO 3 — `subgraph_pitch.py` *(fisier nou)*
Creeaza un subgraf cu un singur nod `draft_pitch` care:
- Apeleaza Groq cu `qualification` + datele lead-ului
- Completeaza `pitch` cu un mesaj scurt de vanzari (max 50 cuvinte)

System prompt sugestie: *"Esti un agent de vanzari. Scrie un email scurt de vanzari adaptat calificarii prospectului."*

---

## TODO 4 — `nodes.py`
Inlocuieste nodurile existente cu:
- `load_lead` — populeaza state cu date hardcodate de test
- `run_qualify_subgraph` — invoca subgraful 1
- `run_pitch_subgraph` — invoca subgraful 2
- `format_output` — printeaza `qualification` + `pitch`

---

## TODO 5 — `main.py`
Actualizeaza graful principal:
```python
graph.add_node("load_lead", load_lead)
graph.add_node("qualify", run_qualify_subgraph)
graph.add_node("pitch", run_pitch_subgraph)
graph.add_node("format", format_output)

graph.set_entry_point("load_lead")
graph.add_edge("load_lead", "qualify")
graph.add_edge("qualify", "pitch")
graph.add_edge("pitch", "format")
```

---

## Rulare
```bash
export GROQ_API_KEY=gsk_...
python -m ex_1_subgraphs.main
```
