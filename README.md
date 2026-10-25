# O4A-Hands-On-CP-SAT
Constraint Programming with CP-SAT - Optimization4All Hands-On Session Series

There is a solver out there that keeps winning OR challenges, and not enough people know about it! In this hands-on session we get to know Google OR-Tools' CP-SAT:

1. **Hello CP-SAT**: a small assignment problem, once in MIP style and once with the global constraints `add_all_different` and `add_element`
2. **Workforce allocation & scheduling** from the [MiniZinc Challenge 2026](https://www.minizinc.org/challenge/2026/results/), built up step by step: fixed start times, time windows, precedences, same team groups and unavailabilities, fairness. At every step we compare a MIP-style formulation with optional interval variables and `add_no_overlap`.

## Notebooks

| Notebook | Description | |
|---|---|---|
| `cp_sat_homework.ipynb` | Homework with gaps, to do before the live session | [Open in Colab](https://colab.research.google.com/github/jpjj/O4A-Hands-On-CP-SAT/blob/main/cp_sat_homework.ipynb) |
| `cp_sat_complete.ipynb` | Complete version that accompanies the talk | [Open in Colab](https://colab.research.google.com/github/jpjj/O4A-Hands-On-CP-SAT/blob/main/cp_sat_complete.ipynb) |

Slides: [jpjsolutions.com/presentations/hands-on-cp-sat](https://jpjsolutions.com/presentations/hands-on-cp-sat/)

## Running locally

```bash
python -m venv .venv
.venv/bin/pip install ortools==9.15.6755 pydantic matplotlib jupyter
.venv/bin/jupyter lab
```

## Data

`data/workforce/` contains instances of the workforce allocation & scheduling problem by Ignace Bleukx (MIT License) from the MiniZinc Challenge 2026, based on Bleukx et al., *Modeling and explaining an industrial workforce allocation and scheduling problem*, CP 2025. They were converted to JSON with 0-based indices by `scripts/convert_mznc.py` (source: [mznc2026_probs.tar.gz](https://www.minizinc.org/challenge/2026/mznc2026_probs.tar.gz)).

`scripts/mznc2026_summary.py` recomputes the challenge scores from the official `results.json` for the charts on the slides.
