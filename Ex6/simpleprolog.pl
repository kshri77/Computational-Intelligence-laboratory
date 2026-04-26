likes(ravi, X) :- food(X).

food(apple).
food(chicken).
food(Y) :- eats(X, Y), \+ killed(X).

eats(ajay, peanuts).
alive(ajay).

eats(rita, X) :- eats(ajay, X).

killed(X) :- \+ alive(X).
