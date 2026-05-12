% Play Tennis dataset written as Prolog facts.
% Each day has weather attributes and one target class.

day(d1).
outlook(d1, sunny).
temperature(d1, hot).
humidity(d1, high).
wind(d1, weak).
play_tennis(d1, no).

day(d2).
outlook(d2, sunny).
temperature(d2, hot).
humidity(d2, high).
wind(d2, strong).
play_tennis(d2, no).

day(d3).
outlook(d3, overcast).
temperature(d3, hot).
humidity(d3, high).
wind(d3, weak).
play_tennis(d3, yes).

day(d4).
outlook(d4, rainy).
temperature(d4, mild).
humidity(d4, high).
wind(d4, weak).
play_tennis(d4, yes).

day(d5).
outlook(d5, rainy).
temperature(d5, cool).
humidity(d5, normal).
wind(d5, weak).
play_tennis(d5, yes).

day(d6).
outlook(d6, rainy).
temperature(d6, cool).
humidity(d6, normal).
wind(d6, strong).
play_tennis(d6, no).

day(d7).
outlook(d7, overcast).
temperature(d7, cool).
humidity(d7, normal).
wind(d7, strong).
play_tennis(d7, yes).

day(d8).
outlook(d8, sunny).
temperature(d8, mild).
humidity(d8, high).
wind(d8, weak).
play_tennis(d8, no).

day(d9).
outlook(d9, sunny).
temperature(d9, cool).
humidity(d9, normal).
wind(d9, weak).
play_tennis(d9, yes).

day(d10).
outlook(d10, rainy).
temperature(d10, mild).
humidity(d10, normal).
wind(d10, weak).
play_tennis(d10, yes).

day(d11).
outlook(d11, sunny).
temperature(d11, mild).
humidity(d11, normal).
wind(d11, strong).
play_tennis(d11, yes).

day(d12).
outlook(d12, overcast).
temperature(d12, mild).
humidity(d12, high).
wind(d12, strong).
play_tennis(d12, yes).

day(d13).
outlook(d13, overcast).
temperature(d13, hot).
humidity(d13, normal).
wind(d13, weak).
play_tennis(d13, yes).

day(d14).
outlook(d14, rainy).
temperature(d14, mild).
humidity(d14, high).
wind(d14, strong).
play_tennis(d14, no).

% Positive and negative examples for the target concept.
positive_example(Day) :-
    play_tennis(Day, yes).

negative_example(Day) :-
    play_tennis(Day, no).
