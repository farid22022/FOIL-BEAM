% Graph dataset from the lecture slide.

edge(1, 2).
edge(1, 3).
edge(3, 6).
edge(4, 2).
edge(4, 6).
edge(6, 5).

path(X, Y) :-
    edge(X, Y).

path(X, Y) :-
    edge(X, Z),
    path(Z, Y).

% Sample queries:
% ?- edge(1,2).
% ?- path(1,5).
% ?- path(4,5).
% ?- path(2,5).
