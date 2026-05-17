import math
from pathlib import Path

from dataset import (
    candidate_literals,
    covered_examples,
    dataset_summary,
    example_pair,
    format_rule,
    load_graph_dataset,
)


def _log_fraction(positive, negative):
    if positive == 0 or positive + negative == 0:
        return None
    return math.log2(positive / (positive + negative))


def foil_gain(p0, n0, p1, n1, t):
    old_value = _log_fraction(p0, n0)
    new_value = _log_fraction(p1, n1)
    if old_value is None or new_value is None:
        return float("-inf")
    return t * (new_value - old_value)


def _gain_text(value):
    if value == float("-inf"):
        return "-inf"
    return f"{value:.4f}"


def learn_foil(positives, negatives, facts, literals):
    uncovered = positives[:]
    learned_rules = []
    output = [
        "FOIL Learning Started",
        "Target Predicate: path(X,Y)",
        f"Positive examples: {len(positives)}",
        f"Negative examples: {len(negatives)}",
        "",
    ]

    rule_number = 1

    while uncovered:
        rule = []
        output.append(f"Learning Rule {rule_number}")
        output.append(f"Initial Rule: {format_rule(rule)}")
        output.append("")

        while True:
            current_pos = covered_examples(rule, uncovered, facts)
            current_neg = covered_examples(rule, negatives, facts)
            p0 = len(current_pos)
            n0 = len(current_neg)

            if n0 == 0:
                break

            best_literal = None
            best_gain = float("-inf")
            best_pos = []
            best_neg = []

            output.append(f"Current coverage: p0={p0}, n0={n0}")
            output.append("Candidate literals and FOIL Gain:")

            for literal in literals:
                if literal in rule:
                    continue

                new_rule = rule + [literal]
                new_pos = covered_examples(new_rule, uncovered, facts)
                new_neg = covered_examples(new_rule, negatives, facts)
                p1 = len(new_pos)
                n1 = len(new_neg)
                gain = foil_gain(p0, n0, p1, n1, p1)

                output.append(
                    f"  Candidate Literal: {str(literal):12s} "
                    f"p1={p1:2d}, n1={n1:2d}, FOIL Gain={_gain_text(gain)}"
                )

                if gain > best_gain:
                    best_literal = literal
                    best_gain = gain
                    best_pos = new_pos
                    best_neg = new_neg

            if best_literal is None or best_gain <= 0:
                output.append("No useful literal found. Stopping this rule.")
                break

            rule.append(best_literal)
            output.append(f"Selected Literal: {best_literal}")
            output.append(f"Selected FOIL Gain: {_gain_text(best_gain)}")
            output.append(f"Updated Rule: {format_rule(rule)}")
            output.append(f"Updated coverage: p1={len(best_pos)}, n1={len(best_neg)}")
            output.append("")

        covered = covered_examples(rule, uncovered, facts)
        if not covered:
            output.append("The rule did not cover a new positive example.")
            break

        covered_pairs = {example_pair(example) for example in covered}
        uncovered = [
            example for example in uncovered if example_pair(example) not in covered_pairs
        ]

        learned_rules.append(rule)
        output.append(f"Learned Rule {rule_number}:")
        output.append(format_rule(rule))
        output.append(f"Positive examples covered: {len(covered)}")
        output.append(f"Remaining positive examples: {len(uncovered)}")
        output.append("")
        rule_number += 1

    output.append("Final Learned Rules:")
    for rule in learned_rules:
        output.append(format_rule(rule))
    output.append("")
    output.append("FOIL Learning Finished")

    return learned_rules, "\n".join(output)


def run_foil():
    nodes, edges, positives, negatives, facts = load_graph_dataset()
    literals = candidate_literals()
    _, text = learn_foil(positives, negatives, facts, literals)

    full_output = dataset_summary(nodes, edges, positives, negatives) + "\n\n" + text
    output_path = Path(__file__).resolve().parents[1] / "output" / "foil_output.txt"
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(full_output, encoding="utf-8")
    print(full_output)


if __name__ == "__main__":
    run_foil()
