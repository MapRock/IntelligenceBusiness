% pkl file name: c:/MapRock/IntelligenceBusiness/book_code/appendix_c/decision_tree.pkl

:- dynamic p/6.

p(_, _, Petallengthcm, _, setosa, 0.33) :- Petallengthcm =< 2.45.
p(_, _, Petallengthcm, Petalwidthcm, versicolor, 0.00) :- Petallengthcm >  2.45, Petalwidthcm =< 1.75, Petallengthcm =< 4.95, Petalwidthcm =< 1.65.
p(_, _, Petallengthcm, Petalwidthcm, virginica, 0.50) :- Petallengthcm >  2.45, Petalwidthcm =< 1.75, Petallengthcm =< 4.95, Petalwidthcm >  1.65.
p(_, _, Petallengthcm, Petalwidthcm, virginica, 0.09) :- Petallengthcm >  2.45, Petalwidthcm =< 1.75, Petallengthcm >  4.95, Petalwidthcm =< 1.55.
p(_, _, Petallengthcm, Petalwidthcm, versicolor, 0.98) :- Petallengthcm >  2.45, Petalwidthcm =< 1.75, Petallengthcm >  4.95, Petalwidthcm >  1.55, Petallengthcm =< 5.45.
p(_, _, Petallengthcm, Petalwidthcm, virginica, 0.00) :- Petallengthcm >  2.45, Petalwidthcm =< 1.75, Petallengthcm >  4.95, Petalwidthcm >  1.55, Petallengthcm >  5.45.
p(Sepallengthcm, _, Petallengthcm, Petalwidthcm, versicolor, 0.00) :- Petallengthcm >  2.45, Petalwidthcm >  1.75, Petallengthcm =< 4.85, Sepallengthcm =< 5.95.
p(Sepallengthcm, _, Petallengthcm, Petalwidthcm, virginica, 0.67) :- Petallengthcm >  2.45, Petalwidthcm >  1.75, Petallengthcm =< 4.85, Sepallengthcm >  5.95.
p(_, _, Petallengthcm, Petalwidthcm, virginica, 1.00) :- Petallengthcm >  2.45, Petalwidthcm >  1.75, Petallengthcm >  4.85.
