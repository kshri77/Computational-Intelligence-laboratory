member(X, [X|_]).
member(X, [_|Tail]) :- member(X, Tail).

% 2. Union
union([], Set2, Set2).
union([H|T], Set2, Result) :-
    member(H, Set2), !,
    union(T, Set2, Result).
union([H|T], Set2, [H | Result]) :-
    union(T, Set2, Result).

% 3. Intersection
intersection([], _, []).
intersection([H|T], Set2, [H | Result]) :-
    member(H, Set2), !,
    intersection(T, Set2, Result).
intersection([_|T], Set2, Result) :-
    intersection(T, Set2, Result).

% 4. Difference (A - B)
difference([], _, []).
difference([H|T], Set2, Result) :-
    member(H, Set2), !,
    difference(T, Set2, Result).
difference([H|T], Set2, [H | Result]) :-
    difference(T, Set2, Result).

% 5. Subset
subset([], _).
subset([H|T], Set2) :-
    member(H, Set2),
    subset(T, Set2).

% 6. Cardinality
cardinality([], 0).
cardinality([_|T], Count) :-
    cardinality(T, SubCount),
    Count is SubCount + 1.

% 7. Equivalent Sets
equivalent(Set1, Set2) :-
    cardinality(Set1, C),
    cardinality(Set2, C).

% 8. Equal Sets
equal(Set1, Set2) :-
    subset(Set1, Set2),
    subset(Set2, Set1).
