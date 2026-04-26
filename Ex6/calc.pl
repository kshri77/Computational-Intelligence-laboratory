
calculate(+,A,B,R):- R is A+B.
calculate(-,A,B,R):- R is A-B.
calculate(*,A,B,R):- R is A*B.
calculate(/,A,B,R):- B =\= 0, R is A/B.
calculate(mod,A,B,R):- B =\= 0, R is A mod B. % Changed % to mod

menu:-
  nl, write("1.ADD"),
  nl, write("2.SUB"),
  nl, write("3.MUL"),
  nl, write("4.DIV"),
  nl, write("5.MOD"),
  nl, write("6.EXIT"),
  nl, write("Enter ur choice: "),
  read(Ch), % Capitalized Ch
  process(Ch).

process(1):-
   write("Enter num1: "), read(A),
   write("Enter num2: "), read(B),
   calculate(+,A,B,R),
   write("Result: "), write(R).

process(2):-
   write("Enter num1: "), read(A),
   write("Enter num2: "), read(B),
   calculate(-,A,B,R),
   write("Result: "), write(R).

process(3):-
   write("Enter num1: "), read(A),
   write("Enter num2: "), read(B),
   calculate(*,A,B,R),
   write("Result: "), write(R).

process(4):-
   write("Enter num1: "), read(A),
   write("Enter num2: "), read(B),
   (B =:= 0 -> write("Division by zero error")),
   calculate(/,A,B,R),
   write("Result: "), write(R).

process(5):-
   write("Enter num1: "), read(A),
   write("Enter num2: "), read(B),
    (B =:= 0 -> write("Modulo by zero error")),
   calculate(mod,A,B,R), % Changed to mod
   write("Result: "), write(R).

process(6):- write("Exiting...").
