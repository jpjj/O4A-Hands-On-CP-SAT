# O4A-Hands-On-CP-SAT
Constraint Programming with CP-SAT - Optimization4All Hands-On Session Series

There is a solver out there that keeps winning OR challenges, and not enough people know about it! In this hands-on session we model three problems from the [MiniZinc Challenge 2026](https://www.minizinc.org/challenge/2026/results/) with Google OR-Tools' CP-SAT:

1. **Nonogram**: Booleans, enforcement literals and the global constraint `add_automaton`
2. **Workforce allocation & scheduling**: optional interval variables and `add_no_overlap`, compared against a Big-M MIP (Pyomo + HiGHS)
3. **Orthorio**: routing conveyor belts in Factorio with `add_circuit`

## Notebooks

| Notebook | Description | |
|---|---|---|
| `cp_sat_homework.ipynb` | Homework with gaps, to do before the live session | [Open in Colab](https://colab.research.google.com/github/jpjj/O4A-Hands-On-CP-SAT/blob/main/cp_sat_homework.ipynb) |
| `cp_sat_complete.ipynb` | Complete version that accompanies the talk | [Open in Colab](https://colab.research.google.com/github/jpjj/O4A-Hands-On-CP-SAT/blob/main/cp_sat_complete.ipynb) |

Slides: [jpjsolutions.com/presentations/hands-on-cp-sat](https://jpjsolutions.com/presentations/hands-on-cp-sat/)

## Running locally

```bash
python -m venv .venv
.venv/bin/pip install ortools==9.15.6755 highspy==1.12.0 pyomo pydantic matplotlib jupyter
.venv/bin/jupyter lab
```

OR-Tools ships its own copy of HiGHS. `highspy` 1.12.0 is compatible with it; newer versions crash when both are imported in the same process.

## Data

`data/` contains instances of the MiniZinc Challenge 2026, converted to JSON with 0-based indices by `scripts/convert_mznc.py` (source: [mznc2026_probs.tar.gz](https://www.minizinc.org/challenge/2026/mznc2026_probs.tar.gz)):

- `orthorio/`: Orthorio by Julia Dijkstra (MIT License)
- `workforce/`: workforce allocation & scheduling by Ignace Bleukx (MIT License), based on Bleukx et al., *Modeling and explaining an industrial workforce allocation and scheduling problem*, CP 2025
- `nonogram/`: nonogram instances of the MiniZinc Challenge 2026 benchmark set

`scripts/mznc2026_summary.py` recomputes the challenge scores from the official `results.json` for the charts on the slides.
