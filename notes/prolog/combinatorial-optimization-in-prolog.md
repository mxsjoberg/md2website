# Combinatorial Optimization in Prolog

<mark>October 2020</mark>

A farmer have chickens and cows for a total of 30 animals, the animals have 74 legs in total. 

How many chickens does the farmer have?

```prolog
?- Chickens + Cows #= 30,
|    Chickens * 2 + Cows * 4 #= 74,
|    Chickens in 0..sup,
|    Cows in 0..sup.
% Chickens = 23,
% Cows = 7.
```