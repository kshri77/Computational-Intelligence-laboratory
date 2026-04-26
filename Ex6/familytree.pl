male(motilal).
male(jawaharlal).
male(feroze).
male(rajiv).
male(sanjay).
male(rahul).
male(varun).

female(swarup).
female(kamala).
female(vijaya_lakshmi).
female(krishna).
female(indira).
female(sonia).
female(maneka).
female(priyanka).

parent(motilal, jawaharlal).
parent(motilal, vijaya_lakshmi).
parent(motilal, krishna).
parent(swarup, jawaharlal).
parent(swarup, vijaya_lakshmi).
parent(swarup, krishna).
parent(jawaharlal, indira).
parent(kamala, indira).
parent(feroze, rajiv).
parent(feroze, sanjay).
parent(indira, rajiv).
parent(indira, sanjay).
parent(rajiv, rahul).
parent(rajiv, priyanka).
parent(sonia, rahul).
parent(sonia, priyanka).
parent(sanjay, varun).
parent(maneka, varun).

father(X, Y) :- male(X), parent(X, Y).
mother(X, Y) :- female(X), parent(X, Y).

spouse(X, Y) :- parent(X, Z), parent(Y, Z), X \= Y.

sibling(X, Y) :- setof(Z, (parent(Z, X), parent(Z, Y)), [_|_]), X \= Y.
brother(X, Y) :- male(X), sibling(X, Y).
sister(X, Y) :- female(X), sibling(X, Y).

grandfather(X, Y) :- father(X, Z), parent(Z, Y).
grandmother(X, Y) :- mother(X, Z), parent(Z, Y).

son(X, Y) :- male(X), parent(Y, X).
daughter(X, Y) :- female(X), parent(Y, X).

grandson(X, Y) :- male(X), (grandfather(Y, X) ; grandmother(Y, X)).
granddaughter(X, Y) :- female(X), (grandfather(Y, X) ; grandmother(Y, X)).

uncle(X, Y) :- male(X), sibling(X, Z), parent(Z, Y).
aunt(X, Y) :- female(X), sibling(X, Z), parent(Z, Y).

nephew(X, Y) :- male(X), sibling(Y, Z), parent(Z, X).
niece(X, Y) :- female(X), sibling(Y, Z), parent(Z, X).

cousin(X, Y) :- parent(A, X), parent(B, Y), sibling(A, B).

relation(father, X, Y) :- father(X, Y).
relation(mother, X, Y) :- mother(X, Y).
relation(grandfather, X, Y) :- grandfather(X, Y).
relation(grandmother, X, Y) :- grandmother(X, Y).
relation(granddaughter, X, Y) :- granddaughter(X, Y)
