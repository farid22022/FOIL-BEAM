# FOIL and Beam Search Assignment Project

Topic: **FOIL Algorithm and Beam Search Algorithm Implementation on a Given Dataset**

This project is prepared as a university assignment-ready implementation. It uses the **Play Tennis** dataset to demonstrate:

- FOIL-style rule learning in Python
- FOIL-style logical rules in Prolog
- Beam Search implementation in Python
- Dataset files, output files, and full documentation

## Project Structure

```text
foil-beam-assignment/
|-- dataset/
|   |-- data.csv
|   `-- facts.pl
|-- foil/
|   |-- foil_python.py
|   `-- foil_prolog.pl
|-- beam_search/
|   `-- beam_search.py
|-- outputs/
|   |-- foil_python_output.txt
|   |-- foil_prolog_output.txt
|   `-- beam_search_output.txt
|-- documentation/
|   `-- assignment_report.md
`-- README.md
```

## Dataset

The project uses the **Play Tennis** dataset.

Input attributes:

- `outlook`
- `temperature`
- `humidity`
- `wind`

Target/output column:

- `play_tennis`

Example row:

```text
Outlook = sunny
Temperature = cool
Humidity = normal
Wind = weak
Output = yes
```

## Run FOIL in Python

From inside the `foil-beam-assignment` folder, run:

```powershell
python foil\foil_python.py
```

Save output:

```powershell
python foil\foil_python.py > outputs\foil_python_output.txt
```

The program prints:

- Positive examples
- Negative examples
- Candidate rules
- Selected FOIL-style rules
- Classification result
- Accuracy

## Run Beam Search in Python

From inside the `foil-beam-assignment` folder, run:

```powershell
python beam_search\beam_search.py
```

Save output:

```powershell
python beam_search\beam_search.py > outputs\beam_search_output.txt
```

The program prints:

- Initial state
- Beam width
- Candidate states
- Scoring values
- Selected beam states at each level
- Final best rule

## Run Prolog Code

Install SWI-Prolog first:

```text
https://www.swi-prolog.org/
```

Open SWI-Prolog from the project folder and load the Prolog file:

```prolog
?- ['foil/foil_prolog.pl'].
```

Sample queries:

```prolog
?- play_tennis(d9, yes).
?- classify(d9, Result).
?- test_all.
?- accuracy.
?- halt.
```

Expected result for `d9`:

```text
Result = yes.
```

## Learned FOIL Rules

The final FOIL-style rules are:

```text
IF outlook = overcast THEN play_tennis = yes
IF outlook = rainy AND wind = weak THEN play_tennis = yes
IF outlook = sunny AND humidity = normal THEN play_tennis = yes
OTHERWISE play_tennis = no
```

## Output Files

Generated output files are stored in:

```text
outputs/
```

Files:

- `outputs/foil_python_output.txt`
- `outputs/beam_search_output.txt`
- `outputs/foil_prolog_output.txt`

These files can be used for assignment screenshots or hard-copy result sections.

## Documentation

Full assignment documentation is available here:

```text
documentation/assignment_report.md
```

The report includes:

- English explanation
- Bangla explanation
- Dataset table
- FOIL algorithm explanation
- Beam Search explanation
- Prolog beginner guide
- Code listings
- Commands
- Expected outputs

## Requirements

Python:

```text
Python 3.10 or later
```

Prolog:

```text
SWI-Prolog
```

No external Python libraries are required.
