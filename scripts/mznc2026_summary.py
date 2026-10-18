"""
Summarize the official MiniZinc Challenge 2026 results for the slides.

Usage:
    python scripts/mznc2026_summary.py <output.json> [path/to/results.json]

Without a local copy, results.json (~40 MB) is downloaded from
https://www.minizinc.org/challenge/2026/results.json

Scores are recomputed with the challenge's complete (Borda) scoring, including the
reference entries that are not eligible for prizes (Gurobi, CPLEX, HiGHS, ...).
"""

import json
import sys
import urllib.request
from pathlib import Path

RESULTS_URL = "https://www.minizinc.org/challenge/2026/results.json"

NAMES = {
    "atlantis": "Atlantis", "cbc": "Cbc", "choco-solver__cp_": "Choco (CP)", "choco-solver__cp_lcg_": "Choco (CP+LCG)",
    "chuffed": "Chuffed", "cp_optimizer": "IBM CP Optimizer", "cplex": "CPLEX", "crusher": "Crusher",
    "gecode": "Gecode", "gecode___scheduling_portfolio__experimental_": "Gecode + Scheduling",
    "gurobi_12": "Gurobi 12", "highs": "HiGHS", "huub": "Huub", "huub__difference_logic_": "Huub (Diff. Logic)",
    "jacop": "JaCoP", "nucs": "NuCS", "or-tools_cp-sat": "OR-Tools CP-SAT", "or-tools_cp-sat-ls": "CP-SAT LS",
    "picatsat": "PicatSAT", "pumpkin": "Pumpkin", "qiuqi-mixsolver": "QiuQi-MIXSolver", "sabori_csp": "Sabori CSP",
    "scip": "SCIP", "sicstus_prolog": "SICStus Prolog", "thornbill": "Thornbill", "yuck": "Yuck",
}
MIP = {"cbc", "cplex", "gurobi_12", "highs", "scip"}
REFERENCE = {"cbc", "chuffed", "cp_optimizer", "cplex", "gecode", "gecode_dexter",
             "gecode___scheduling_portfolio__experimental_", "gurobi_12", "highs", "huub",
             "huub__difference_logic_", "minifolio", "scip", "thornbill"}


def base_name(solver_id: str) -> str:
    return solver_id.rsplit("-", 1)[0]


def ranking(r: dict, flag: str) -> list[dict]:
    members = [i for i, f in enumerate(r[flag]) if f]
    rows = []
    for i in members:
        score = sum(r["scores"][i][j][k] for j in members if j != i for k in range(len(r["benchmarks"])))
        name = base_name(r["solvers"][i])
        rows.append({
            "solver": NAMES.get(name, name),
            "score": round(score, 1),
            "group": "cpsat" if name == "or-tools_cp-sat" else "mip" if name in MIP else "other",
            "reference": name in REFERENCE,
        })
    return sorted(rows, key=lambda row: -row["score"])


def head_to_head(r: dict, a: str, b: str) -> list[dict]:
    i, j = r["solvers"].index(a), r["solvers"].index(b)
    rows = []
    for p, problem in enumerate(r["problems"]):
        instances = r["instances"][p]
        rows.append({
            "problem": problem,
            "a": round(sum(r["scores"][i][j][k] for k in instances), 2),
            "b": round(sum(r["scores"][j][i][k] for k in instances), 2),
        })
    return sorted(rows, key=lambda row: row["a"] - row["b"])


if __name__ == "__main__":
    output = Path(sys.argv[1])
    if len(sys.argv) > 2:
        data = json.loads(Path(sys.argv[2]).read_text())
    else:
        with urllib.request.urlopen(RESULTS_URL) as response:
            data = json.loads(response.read())
    r = data["results"]
    summary = {
        "source": RESULTS_URL,
        "ranking_free": ranking(r, "free_solvers"),
        "ranking_parallel": ranking(r, "par_solvers"),
        "cpsat_vs_gurobi_free": head_to_head(r, "or-tools_cp-sat-free", "gurobi_12-free"),
    }
    output.write_text(json.dumps(summary, indent=1))
    print(f"wrote {output}")
