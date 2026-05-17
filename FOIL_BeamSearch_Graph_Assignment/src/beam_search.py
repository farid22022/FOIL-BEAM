from pathlib import Path

from dataset import (
    candidate_literals,
    covered_examples,
    dataset_summary,
    example_pair,
    format_rule,
    load_graph_dataset,
)


def evaluate_rule(rule, positives, negatives, facts):
    pos = covered_examples(rule, positives, facts)
    neg = covered_examples(rule, negatives, facts)
    p = len(pos)
    n = len(neg)
    total = p + n

    accuracy = p / total if total else 0.0
    coverage = p / len(positives) if positives else 0.0

    return {
        "p": p,
        "n": n,
        "accuracy": accuracy,
        "coverage": coverage,
    }


def _rule_key(rule):
    return tuple(str(literal) for literal in rule)


def _sort_key(item):
    _, score = item
    return (
        score["accuracy"],
        score["coverage"],
        score["p"],
        -score["n"],
    )


def _candidate_examples(candidates):
    wanted = [
        "path(X,Y) :- edge(X,Y).",
        "path(X,Y) :- edge(X,Z).",
        "path(X,Y) :- edge(X,Z), edge(Z,Y).",
        "path(X,Y) :- edge(X,Z), path(Z,Y).",
    ]
    available = {format_rule(rule) for rule, _ in candidates}
    return [rule for rule in wanted if rule in available]


def beam_search_one_rule(positives, negatives, facts, literals, beam_width=3, max_depth=3):
    beam = [[]]
    best_rule = []
    best_score = evaluate_rule(best_rule, positives, negatives, facts)
    seen = {()}
    lines = []

    for depth in range(1, max_depth + 1):
        candidates = []

        for rule in beam:
            for literal in literals:
                if literal in rule:
                    continue

                new_rule = rule + [literal]
                key = _rule_key(new_rule)
                if key in seen:
                    continue

                seen.add(key)
                score = evaluate_rule(new_rule, positives, negatives, facts)
                candidates.append((new_rule, score))

        if not candidates:
            break

        candidates.sort(key=_sort_key, reverse=True)
        beam = [rule for rule, _ in candidates[:beam_width]]

        lines.append(f"Iteration {depth}: Candidate rules generated = {len(candidates)}")
        examples = _candidate_examples(candidates)
        if examples:
            lines.append("Generated candidate examples:")
            for rule_text in examples:
                lines.append(f"  - {rule_text}")
        lines.append(f"Top {beam_width} candidate rules:")

        for index, (rule, score) in enumerate(candidates[:beam_width], start=1):
            lines.append(
                f"  {index}. {format_rule(rule)} "
                f"Accuracy={score['accuracy']:.4f}, "
                f"Coverage={score['coverage']:.4f}, "
                f"p={score['p']}, n={score['n']}"
            )

            if _sort_key((rule, score)) > _sort_key((best_rule, best_score)):
                best_rule = rule
                best_score = score

        lines.append("")

        if best_score["accuracy"] == 1.0 and best_score["coverage"] == 1.0:
            break

    return best_rule, best_score, lines


def learn_with_beam_search(
    positives,
    negatives,
    facts,
    literals,
    beam_width=3,
    max_depth=3,
):
    uncovered = positives[:]
    learned_rules = []
    output = [
        "General-to-Specific Beam Search Started",
        "Target Predicate: path(X,Y)",
        f"Beam width: {beam_width}",
        "",
    ]

    rule_number = 1

    while uncovered:
        output.append(f"Searching Rule {rule_number}")
        output.append("Start Rule: path(X,Y) :- true.")

        rule, score, detail_lines = beam_search_one_rule(
            uncovered,
            negatives,
            facts,
            literals,
            beam_width=beam_width,
            max_depth=max_depth,
        )
        output.extend(detail_lines)

        covered = covered_examples(rule, uncovered, facts)
        if not covered:
            output.append("No useful rule found.")
            break

        covered_pairs = {example_pair(example) for example in covered}
        uncovered = [
            example for example in uncovered if example_pair(example) not in covered_pairs
        ]

        learned_rules.append(rule)
        output.append(f"Selected Rule {rule_number}:")
        output.append(format_rule(rule))
        output.append(
            f"Accuracy={score['accuracy']:.4f}, Coverage={score['coverage']:.4f}, "
            f"p={score['p']}, n={score['n']}"
        )
        output.append(f"Remaining positive examples: {len(uncovered)}")
        output.append("")
        rule_number += 1

    output.append("Final Selected Rules:")
    for rule in learned_rules:
        output.append(format_rule(rule))
    output.append("")
    output.append("Beam Search Finished")

    return learned_rules, "\n".join(output)


def run_beam_search():
    nodes, edges, positives, negatives, facts = load_graph_dataset()
    literals = candidate_literals()
    _, text = learn_with_beam_search(
        positives,
        negatives,
        facts,
        literals,
        beam_width=3,
        max_depth=3,
    )

    full_output = dataset_summary(nodes, edges, positives, negatives) + "\n\n" + text
    output_path = Path(__file__).resolve().parents[1] / "output" / "beam_search_output.txt"
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(full_output, encoding="utf-8")
    print(full_output)


if __name__ == "__main__":
    run_beam_search()
