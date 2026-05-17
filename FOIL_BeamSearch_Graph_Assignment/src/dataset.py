from dataclasses import dataclass
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


@dataclass(frozen=True)
class Literal:
    predicate: str
    arguments: tuple

    def __str__(self):
        return f"{self.predicate}({','.join(self.arguments)})"


def _load_raw_dataset():
    project_root = Path(__file__).resolve().parents[1]
    data_path = project_root / "data" / "graph_dataset.py"
    spec = spec_from_file_location("graph_dataset", data_path)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_graph_dataset():
    raw = _load_raw_dataset()
    nodes = list(raw.NODES)
    edges = list(raw.EDGES)
    positives = [{"X": x, "Y": y} for x, y in raw.POSITIVE_PATHS]
    positive_pairs = set(raw.POSITIVE_PATHS)

    negatives = []
    for x in nodes:
        for y in nodes:
            if (x, y) not in positive_pairs:
                negatives.append({"X": x, "Y": y})

    facts = {
        "edge": set(edges),
        # During learning, known positive path facts are used to allow a
        # simple recursive candidate literal path(Z,Y).
        "path": set(raw.POSITIVE_PATHS),
    }

    return nodes, edges, positives, negatives, facts


def candidate_literals():
    return [
        Literal("edge", ("X", "Y")),
        Literal("edge", ("X", "Z")),
        Literal("edge", ("Z", "Y")),
        Literal("path", ("Z", "Y")),
        Literal("path", ("X", "Z")),
    ]


def apply_literal(literal, bindings, facts):
    new_bindings = []
    fact_set = facts.get(literal.predicate, set())

    for binding in bindings:
        for fact in fact_set:
            if len(fact) != len(literal.arguments):
                continue

            possible = dict(binding)
            ok = True

            for arg, value in zip(literal.arguments, fact):
                if arg in possible and possible[arg] != value:
                    ok = False
                    break
                possible[arg] = value

            if ok:
                new_bindings.append(possible)

    return new_bindings


def rule_bindings(rule, example, facts):
    bindings = [dict(example)]
    for literal in rule:
        bindings = apply_literal(literal, bindings, facts)
        if not bindings:
            break
    return bindings


def rule_covers(rule, example, facts):
    return bool(rule_bindings(rule, example, facts))


def covered_examples(rule, examples, facts):
    return [example for example in examples if rule_covers(rule, example, facts)]


def format_rule(rule):
    if not rule:
        return "path(X,Y) :- true."
    body = ", ".join(str(literal) for literal in rule)
    return f"path(X,Y) :- {body}."


def example_pair(example):
    return example["X"], example["Y"]


def dataset_summary(nodes, edges, positives, negatives):
    lines = [
        "Dataset Preparation",
        "-------------------",
        f"Nodes: {', '.join(str(node) for node in nodes)}",
        "Background predicate: edge(X,Y)",
        "Target predicate: path(X,Y)",
        "",
        "Edges:",
    ]
    lines.extend(f"- edge({x},{y})." for x, y in edges)
    lines.extend(
        [
            "",
            f"Positive path examples: {len(positives)}",
            f"Negative path examples: {len(negatives)}",
            "Closed-world assumption: pairs not listed as positive paths are negative.",
        ]
    )
    return "\n".join(lines)
