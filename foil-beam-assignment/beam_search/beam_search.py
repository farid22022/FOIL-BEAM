"""
Beam Search demonstration using the Play Tennis dataset.

The search space contains possible IF-rules such as:
IF outlook = rainy AND wind = weak THEN play_tennis = yes

Beam Search does not keep every candidate. At each level it keeps only the
best few candidates according to a scoring function.
"""

from __future__ import annotations

import csv
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "dataset" / "data.csv"
TARGET_COLUMN = "play_tennis"
POSITIVE_VALUE = "yes"
ATTRIBUTES = ["outlook", "temperature", "humidity", "wind"]
BEAM_WIDTH = 3
MAX_DEPTH = 2


Condition = tuple[str, str]
State = tuple[Condition, ...]


def load_dataset(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def get_domains(rows: list[dict[str, str]]) -> dict[str, list[str]]:
    return {
        attribute: sorted({row[attribute] for row in rows})
        for attribute in ATTRIBUTES
    }


def normalize_state(state: State) -> State:
    return tuple(sorted(state, key=lambda item: ATTRIBUTES.index(item[0])))


def state_text(state: State) -> str:
    if not state:
        return "TRUE"
    return " AND ".join(f"{attribute} = {value}" for attribute, value in state)


def covers(row: dict[str, str], state: State) -> bool:
    return all(row[attribute] == value for attribute, value in state)


def evaluate_state(rows: list[dict[str, str]], state: State) -> dict[str, float | int]:
    covered = [row for row in rows if covers(row, state)]
    positive = [row for row in covered if row[TARGET_COLUMN] == POSITIVE_VALUE]
    negative = [row for row in covered if row[TARGET_COLUMN] != POSITIVE_VALUE]
    total_positive = sum(1 for row in rows if row[TARGET_COLUMN] == POSITIVE_VALUE)

    precision = len(positive) / len(covered) if covered else 0.0
    recall = len(positive) / total_positive if total_positive else 0.0

    # This score prefers accurate rules, but still rewards rules that cover
    # several positive examples. Pure rules get a small bonus.
    score = (0.70 * precision) + (0.30 * recall)
    if negative == [] and positive:
        score += 0.05
    score -= 0.02 * max(0, len(state) - 1)

    return {
        "positive": len(positive),
        "negative": len(negative),
        "covered": len(covered),
        "precision": precision,
        "recall": recall,
        "score": score,
    }


def expand_state(state: State, domains: dict[str, list[str]]) -> list[State]:
    used_attributes = {attribute for attribute, _ in state}
    children: list[State] = []

    for attribute in ATTRIBUTES:
        if attribute in used_attributes:
            continue
        for value in domains[attribute]:
            child = normalize_state(state + ((attribute, value),))
            children.append(child)

    return children


def rank_states(rows: list[dict[str, str]], states: list[State]) -> list[tuple[State, dict[str, float | int]]]:
    unique_states = sorted(set(states), key=state_text)
    scored = [(state, evaluate_state(rows, state)) for state in unique_states]
    scored.sort(
        key=lambda item: (
            item[1]["score"],
            item[1]["positive"],
            -len(item[0]),
            state_text(item[0]),
        ),
        reverse=True,
    )
    return scored


def print_state(prefix: str, state: State, stats: dict[str, float | int]) -> None:
    print(
        f"{prefix}IF {state_text(state)} THEN play_tennis = yes | "
        f"pos={stats['positive']}, neg={stats['negative']}, "
        f"precision={stats['precision']:.2f}, recall={stats['recall']:.2f}, "
        f"score={stats['score']:.3f}"
    )


def beam_search(rows: list[dict[str, str]]) -> State:
    domains = get_domains(rows)
    beam: list[State] = [tuple()]
    best_state: State = tuple()
    best_stats = evaluate_state(rows, best_state)

    print("Beam Search for a Good Play-Tennis Rule")
    print("=======================================")
    print(f"Dataset: {DATA_PATH}")
    print(f"Initial state: IF TRUE THEN play_tennis = yes")
    print(f"Beam width: {BEAM_WIDTH}")
    print(f"Maximum depth: {MAX_DEPTH}")
    print("Scoring function: 0.70 * precision + 0.30 * recall + purity bonus")
    print()

    for depth in range(1, MAX_DEPTH + 1):
        print(f"Level {depth}: expand current beam")
        candidates: list[State] = []
        for state in beam:
            candidates.extend(expand_state(state, domains))

        ranked = rank_states(rows, candidates)
        print("Candidate states, sorted by score:")
        for state, stats in ranked[:8]:
            print_state("  ", state, stats)

        beam = [state for state, _ in ranked[:BEAM_WIDTH]]
        print("Selected states kept in the beam:")
        for state in beam:
            stats = evaluate_state(rows, state)
            print_state("  ", state, stats)
            if (
                stats["score"] > best_stats["score"]
                or (
                    stats["score"] == best_stats["score"]
                    and len(state) < len(best_state)
                )
            ):
                best_state = state
                best_stats = stats
        print()

    print("Final Result")
    print("============")
    print_state("Best rule found: ", best_state, best_stats)
    print("Meaning: if the condition is true, predict play_tennis = yes.")
    print("Otherwise, use the default prediction play_tennis = no.")
    return best_state


def main() -> None:
    rows = load_dataset(DATA_PATH)
    beam_search(rows)


if __name__ == "__main__":
    main()
