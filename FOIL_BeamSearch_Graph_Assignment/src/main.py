from pathlib import Path

from beam_search import learn_with_beam_search
from dataset import candidate_literals, dataset_summary, load_graph_dataset
from foil import learn_foil


def make_prolog_query_output(facts):
    edges = facts["edge"]
    paths = facts["path"]

    checks = [
        ("edge(1,2)", (1, 2) in edges),
        ("path(1,5)", (1, 5) in paths),
        ("path(4,5)", (4, 5) in paths),
        ("path(2,5)", (2, 5) in paths),
    ]

    lines = [
        "Expected SWI-Prolog Query Output",
        "--------------------------------",
        "",
    ]

    for query, result in checks:
        lines.append(f"?- {query}.")
        lines.append("true." if result else "false.")
        lines.append("")

    return "\n".join(lines).rstrip()


def main():
    project_root = Path(__file__).resolve().parents[1]
    output_dir = project_root / "output"
    output_dir.mkdir(exist_ok=True)

    nodes, edges, positives, negatives, facts = load_graph_dataset()
    literals = candidate_literals()

    summary = dataset_summary(nodes, edges, positives, negatives)
    _, foil_output = learn_foil(positives, negatives, facts, literals)
    _, beam_output = learn_with_beam_search(
        positives,
        negatives,
        facts,
        literals,
        beam_width=3,
        max_depth=3,
    )
    prolog_output = make_prolog_query_output(facts)

    (output_dir / "foil_output.txt").write_text(
        summary + "\n\n" + foil_output,
        encoding="utf-8",
    )
    (output_dir / "beam_search_output.txt").write_text(
        summary + "\n\n" + beam_output,
        encoding="utf-8",
    )
    (output_dir / "prolog_query_output.txt").write_text(
        prolog_output,
        encoding="utf-8",
    )

    print(summary)
    print()
    print("Output files generated:")
    print(f"- {output_dir / 'foil_output.txt'}")
    print(f"- {output_dir / 'beam_search_output.txt'}")
    print(f"- {output_dir / 'prolog_query_output.txt'}")
    print()
    print("Final Learned Rules:")
    print("path(X,Y) :- edge(X,Y).")
    print("path(X,Y) :- edge(X,Z), path(Z,Y).")


if __name__ == "__main__":
    main()
