"""
Convert the MiniZinc Challenge 2026 instances used in the hands-on session into plain JSON.

Usage:
    python scripts/convert_mznc.py path/to/mznc2026_probs

The benchmark archive can be downloaded from
https://www.minizinc.org/challenge/2026/mznc2026_probs.tar.gz

All indices in the generated JSON files are 0-based.
"""

import json
import re
import sys
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


# ---------------------------------------------------------------------------
# Nonogram
# ---------------------------------------------------------------------------

def unary_to_blocks(cons: list[int]) -> list[int]:
    """The challenge encodes clues in unary: 1 = filled cell, 0 = gap, -1 = padding.
    Example: [1, 0, 1, 1, 0, 1, -1, -1] -> blocks [1, 2, 1]."""
    blocks, run = [], 0
    for v in cons:
        if v == 1:
            run += 1
        elif v == 0 and run > 0:
            blocks.append(run)
            run = 0
    if run > 0:
        blocks.append(run)
    return blocks


def convert_nonogram(src: Path, dst: Path):
    for file in sorted(src.glob("*.json")):
        raw = json.loads(file.read_text())
        data = {
            "name": file.stem,
            "rows": [unary_to_blocks(r) for r in raw["rows"]],
            "cols": [unary_to_blocks(c) for c in raw["cols"]],
        }
        assert len(data["rows"]) == raw["Y"] and len(data["cols"]) == raw["X"]
        assert sum(map(sum, data["rows"])) == sum(map(sum, data["cols"])), file
        (dst / f"{file.stem}.json").write_text(json.dumps(data))


# ---------------------------------------------------------------------------
# Workforce allocation & scheduling
# ---------------------------------------------------------------------------

def _int_list(text: str) -> list[int]:
    return [int(v) for v in re.findall(r"-?\d+", text)]


def _enum(text: str, name: str) -> list[str]:
    return re.search(rf"{name}\s*=\s*\{{(.*?)\}};", text, re.S).group(1).replace(" ", "").replace("\n", "").split(",")


def _array(text: str, name: str) -> str:
    return re.search(rf"\b{name}\s*=\s*(.*?);", text, re.S).group(1)


def convert_workforce(src: Path, dst: Path):
    for file in sorted(src.glob("*.dzn")):
        text = file.read_text()
        teams = _enum(text, "Team")
        tasks = _enum(text, "Task")
        task_idx = {t: i for i, t in enumerate(tasks)}
        team_idx = {t: i for i, t in enumerate(teams)}

        duration = _int_list(_array(text, "duration"))
        released = _int_list(_array(text, "released"))
        due = _int_list(_array(text, "due"))
        compat_body = re.search(r"compatible = array2d\(Task, Team, \[(.*?)\]\)", text, re.S).group(1)
        compatible = _int_list(compat_body)
        assert len(compatible) == len(tasks) * len(teams)

        groups = [
            [task_idx[t.strip()] for t in g.split(",")]
            for g in re.findall(r"\{(.*?)\}", _array(text, "same_allocation"))
        ]
        precedences = []
        for task, succs in re.findall(r"\(task: (\w+), successors: \{(.*?)\}\)", _array(text, "successors")):
            for s in succs.split(","):
                if s.strip():
                    precedences.append([task_idx[task], task_idx[s.strip()]])
        unavailabilities = [
            {"team": team_idx[team], "start": int(start), "duration": int(dur)}
            for team, start, dur in re.findall(
                r"\(team: (\w+), start_unavailable: (\d+), dur_unavailable: (\d+)\)", _array(text, "calendars")
            )
        ]

        data = {
            "name": file.stem,
            "horizon": int(_array(text, "horizon")),
            "num_teams": len(teams),
            "tasks": [
                {
                    "id": i,
                    "duration": duration[i],
                    "release": released[i],
                    "due": due[i],
                    "compatible_teams": [k for k in range(len(teams)) if compatible[i * len(teams) + k] == 1],
                }
                for i in range(len(tasks))
            ],
            "same_team_groups": groups,
            "precedences": precedences,
            "unavailabilities": unavailabilities,
        }
        (dst / f"{file.stem}.json").write_text(json.dumps(data))


# ---------------------------------------------------------------------------
# Orthorio (Factorio conveyor belts)
# ---------------------------------------------------------------------------

DIRECTIONS = {"^": "N", ">": "E", "v": "S", "<": "W"}


def convert_orthorio(src: Path, dst: Path):
    for file in sorted(src.glob("*.dzn")):
        text = file.read_text()
        height = int(_array(text, "HEIGHT"))
        width = int(_array(text, "WIDTH"))
        tunnel_ranges = [r for r, flag in ((4, "TUNNEL_4"), (6, "TUNNEL_6")) if _array(text, flag) == "true"]

        ports = re.findall(r'\(y:\s*(\d+), x:\s*(\d+), d: "(.)"\)', text)
        assert len(ports) == 2 * int(_array(text, "AGENTS"))
        port = lambda y, x, d: {"row": int(y) - 1, "col": int(x) - 1, "direction": DIRECTIONS[d]}
        belts = [
            {"id": a, "start": port(*ports[2 * a]), "end": port(*ports[2 * a + 1])}
            for a in range(len(ports) // 2)
        ]

        walls_body = _array(text, "walls")
        if "[0 | _ in" in walls_body:
            walls = []
        else:
            flat = _int_list(re.search(r"\[(.*)\]", walls_body, re.S).group(1))
            walls = [[i // width, i % width] for i, v in enumerate(flat) if v == 1]

        data = {
            "name": file.stem,
            "height": height,
            "width": width,
            "tunnel_ranges": tunnel_ranges,
            "walls": walls,
            "belts": belts,
        }
        (dst / f"{file.stem}.json").write_text(json.dumps(data))


if __name__ == "__main__":
    source = Path(sys.argv[1])
    for name, convert, folder in [
        ("nonogram", convert_nonogram, "nonogram"),
        ("workforce", convert_workforce, "workforce-alloc"),
        ("orthorio", convert_orthorio, "orthorio"),
    ]:
        target = DATA_DIR / name
        target.mkdir(parents=True, exist_ok=True)
        convert(source / folder, target)
        print(f"{name}: {len(list(target.glob('*.json')))} instances -> {target}")
