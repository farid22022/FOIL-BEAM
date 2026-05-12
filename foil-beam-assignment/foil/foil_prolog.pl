% FOIL-style learned rules for the Play Tennis dataset.
% Load this file in SWI-Prolog from the foil folder using:
% ?- [foil_prolog].

:- ensure_loaded('../dataset/facts.pl').

% Rule 1:
% If outlook is overcast, tennis is played.
foil_rule(Day) :-
    outlook(Day, overcast).

% Rule 2:
% If outlook is rainy and wind is weak, tennis is played.
foil_rule(Day) :-
    outlook(Day, rainy),
    wind(Day, weak).

% Rule 3:
% If outlook is sunny and humidity is normal, tennis is played.
foil_rule(Day) :-
    outlook(Day, sunny),
    humidity(Day, normal).

% Classification rule.
% If any FOIL rule succeeds, predict yes. Otherwise predict no.
classify(Day, yes) :-
    foil_rule(Day),
    !.
classify(_, no).

% Print a readable explanation for one day.
explain(Day) :-
    outlook(Day, Outlook),
    temperature(Day, Temperature),
    humidity(Day, Humidity),
    wind(Day, Wind),
    classify(Day, Prediction),
    play_tennis(Day, Actual),
    format('~w: outlook=~w, temperature=~w, humidity=~w, wind=~w~n',
           [Day, Outlook, Temperature, Humidity, Wind]),
    format('Predicted: ~w, Actual: ~w~n', [Prediction, Actual]).

% Test every row in the dataset.
test_all :-
    forall(
        day(Day),
        (
            classify(Day, Prediction),
            play_tennis(Day, Actual),
            format('~w -> predicted: ~w, actual: ~w~n',
                   [Day, Prediction, Actual])
        )
    ).

% Count correct predictions.
count_correct(Count) :-
    findall(
        Day,
        (
            day(Day),
            classify(Day, Prediction),
            play_tennis(Day, Prediction)
        ),
        CorrectDays
    ),
    length(CorrectDays, Count).

% Count all dataset rows.
count_total(Count) :-
    findall(Day, day(Day), Days),
    length(Days, Count).

% Print accuracy.
accuracy :-
    count_correct(Correct),
    count_total(Total),
    Percent is Correct * 100 / Total,
    format('Accuracy: ~w/~w (~2f%)~n', [Correct, Total, Percent]).
