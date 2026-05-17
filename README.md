# FOIL and Beam Search Algorithm Implementation on Lecture Graph Dataset

This is a short university assignment project for implementing simplified FOIL and Beam Search algorithms on the graph dataset from the class lecture slide.

The background predicate is:

```prolog
edge(X,Y)
```

The target predicate is:

```prolog
path(X,Y)
```

The final path rules are:

```prolog
path(X,Y) :- edge(X,Y).
path(X,Y) :- edge(X,Z), path(Z,Y).
```

## Dataset

Nodes:

```text
1, 2, 3, 4, 5, 6
```

Edges:

```prolog
edge(1,2).
edge(1,3).
edge(3,6).
edge(4,2).
edge(4,6).
edge(6,5).
```

Positive path examples are stored manually from the lecture graph. Negative examples are generated from all ordered pairs of nodes that are not positive path examples.

## Folder Structure

```text
FOIL_BeamSearch_Graph_Assignment/
|
|-- data/
|   `-- graph_dataset.py
|
|-- src/
|   |-- dataset.py
|   |-- foil.py
|   |-- beam_search.py
|   `-- main.py
|
|-- prolog/
|   `-- graph_path_rules.pl
|
|-- output/
|   |-- foil_output.txt
|   |-- beam_search_output.txt
|   `-- prolog_query_output.txt
|
|-- documentation/
|   `-- assignment_report.md
|
`-- README.md
```

## Commands

Run full project:

```bash
python src/main.py
```

Run FOIL:

```bash
python src/foil.py
```

Run Beam Search:

```bash
python src/beam_search.py
```

Run Prolog:

```bash
swipl
```

Then in SWI-Prolog:

```prolog
?- ['prolog/graph_path_rules.pl'].
?- path(1,5).
?- path(4,5).
?- path(2,5).
```

## Output Files

The Python program generates:

```text
output/foil_output.txt
output/beam_search_output.txt
output/prolog_query_output.txt
```

## 2-Minute Explanation

I used the graph dataset from the lecture slide. The background predicate is `edge(X,Y)`, and the target predicate is `path(X,Y)`. FOIL learned rules by selecting useful literals using FOIL Gain. Beam Search searched candidate path rules using beam width 3. The final rules were `path(X,Y) :- edge(X,Y)` and `path(X,Y) :- edge(X,Z), path(Z,Y)`. Finally, I represented these rules in Prolog and tested path queries.
