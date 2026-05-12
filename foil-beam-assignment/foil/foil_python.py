"""
Simplified FOIL-style rule learner for the Play Tennis dataset.

The program reads dataset/data.csv, separates positive and negative examples,
then learns human-readable IF-THEN rules for play_tennis = yes.
"""

from __future__ import annotations

import csv
import math
from itertools import combinations
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "dataset" / "data.csv"
TARGET_COLUMN = "play_tennis"
POSITIVE_VALUE = "yes"
ATTRIBUTES = ["outlook", "temperature", "humidity", "wind"]


Condition = tuple[str, str]
Rule = tuple[Condition, ...]


def load_dataset(path: Path) -> list[dict[str, str]]:
    """Load the CSV file as a list of dictionaries."""
    with path.open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def get_domains(rows: list[dict[str, str]]) -> dict[str, list[str]]:
    """Collect possible values for each attribute."""
    domains: dict[str, list[str]] = {}
    for attribute in ATTRIBUTES:
        domains[attribute] = sorted({row[attribute] for row in rows})
    return domains


def covers(row: dict[str, str], rule: Rule) -> bool:
    """Return True if a row satisfies every condition in a rule."""
    return all(row[attribute] == value for attribute, value in rule)


def condition_text(rule: Rule) -> str:
    """Convert a rule condition tuple into readable text."""
    return " AND ".join(f"{attribute} = {value}" for attribute, value in rule)


def all_candidate_rules(domains: dict[str, list[str]], max_conditions: int = 2) -> list[Rule]:
    """Generate candidate rules with no repeated attribute."""
    literals = [
        (attribute, value)
        for attribute in ATTRIBUTES
        for value in domains[attribute]
    ]

    candidates: list[Rule] = []
    for size in range(1, max_conditions + 1):
        for combo in combinations(literals, size):
            used_attributes = [attribute for attribute, _ in combo]
            if len(set(used_attributes)) != len(used_attributes):
                continue
            ordered_combo = tuple(
                sorted(combo, key=lambda item: ATTRIBUTES.index(item[0]))
            )
            candidates.append(ordered_combo)
    return sorted(set(candidates), key=condition_text)


def foil_gain(
    remaining_positive_count: int,
    negative_count: int,
    covered_positive_count: int,
    covered_negative_count: int,
) -> float:
    """
    Compute a simple FOIL information gain score.

    Higher score means the rule keeps useful positive examples while removing
    negative examples.
    """
    if covered_positive_count == 0:
        return float("-inf")

    before_precision = remaining_positive_count / (
        remaining_positive_count + negative_count
    )
    after_precision = covered_positive_count / (
        covered_positive_count + covered_negative_count
    )
    return covered_positive_count * (
        math.log2(after_precision) - math.log2(before_precision)
    )


def learn_rules(rows: list[dict[str, str]]) -> list[Rule]:
    """Learn a small set of rules that cover positive examples."""
    domains = get_domains(rows)
    candidates = all_candidate_rules(domains, max_conditions=2)
    positives = [row for row in rows if row[TARGET_COLUMN] == POSITIVE_VALUE]
    negatives = [row for row in rows if row[TARGET_COLUMN] != POSITIVE_VALUE]
    uncovered_positive_ids = {row["id"] for row in positives}
    learned_rules: list[Rule] = []

    print("FOIL-like Rule Learning")
    print("=======================")
    print(f"Dataset: {DATA_PATH}")
    print(f"Positive examples: {', '.join(row['id'] for row in positives)}")
    print(f"Negative examples: {', '.join(row['id'] for row in negatives)}")
    print()

    iteration = 1
    while uncovered_positive_ids:
        print(f"Iteration {iteration}")
        print(
            "Uncovered positive examples: "
            + ", ".join(sorted(uncovered_positive_ids))
        )

        scored_candidates = []
        for rule in candidates:
            covered_remaining_positives = [
                row
                for row in positives
                if row["id"] in uncovered_positive_ids and covers(row, rule)
            ]
            covered_negatives = [row for row in negatives if covers(row, rule)]

            if not covered_remaining_positives:
                continue

            gain = foil_gain(
                remaining_positive_count=len(uncovered_positive_ids),
                negative_count=len(negatives),
                covered_positive_count=len(covered_remaining_positives),
                covered_negative_count=len(covered_negatives),
            )
            scored_candidates.append(
                {
                    "rule": rule,
                    "text": condition_text(rule),
                    "positive_ids": [row["id"] for row in covered_remaining_positives],
                    "negative_ids": [row["id"] for row in covered_negatives],
                    "positive_count": len(covered_remaining_positives),
                    "negative_count": len(covered_negatives),
                    "is_pure": len(covered_negatives) == 0,
                    "length": len(rule),
                    "gain": gain,
                }
            )

        scored_candidates.sort(
            key=lambda item: (
                item["is_pure"],
                item["positive_count"],
                -item["length"],
                item["gain"],
                item["text"],
            ),
            reverse=True,
        )

        print("Top candidate rules:")
        for item in scored_candidates[:5]:
            print(
                f"  IF {item['text']} THEN yes | "
                f"pos={item['positive_count']} {item['positive_ids']}, "
                f"neg={item['negative_count']} {item['negative_ids']}, "
                f"gain={item['gain']:.3f}"
            )

        best = scored_candidates[0]
        learned_rules.append(best["rule"])
        for row_id in best["positive_ids"]:
            uncovered_positive_ids.remove(row_id)

        print(f"Selected rule: IF {best['text']} THEN play_tennis = yes")
        print()
        iteration += 1

    return learned_rules


def predict(row: dict[str, str], rules: list[Rule]) -> str:
    """Predict yes if any learned rule covers the row."""
    for rule in rules:
        if covers(row, rule):
            return "yes"
    return "no"


def print_classification(rows: list[dict[str, str]], rules: list[Rule]) -> None:
    """Print learned rules and predictions for all rows."""
    print("Final Learned Rules")
    print("===================")
    for index, rule in enumerate(rules, start=1):
        print(f"Rule {index}: IF {condition_text(rule)} THEN play_tennis = yes")
    print("Default rule: otherwise play_tennis = no")
    print()

    print("Classification Output")
    print("=====================")
    correct = 0
    for row in rows:
        prediction = predict(row, rules)
        actual = row[TARGET_COLUMN]
        if prediction == actual:
            correct += 1
        print(
            f"{row['id']}: predicted={prediction}, actual={actual}, "
            f"features=({row['outlook']}, {row['temperature']}, "
            f"{row['humidity']}, {row['wind']})"
        )

    accuracy = correct / len(rows) * 100
    print()
    print(f"Accuracy: {correct}/{len(rows)} = {accuracy:.2f}%")


def main() -> None:
    rows = load_dataset(DATA_PATH)
    rules = learn_rules(rows)
    print_classification(rows, rules)


if __name__ == "__main__":
    main()
