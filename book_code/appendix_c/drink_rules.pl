businessmeal(true) :- companion(boss).
businessmeal(true) :- companion(client)
drinkorder(dietcoke) :- context(lunch), person(eugene).
drinkorder(dietcoke) :- context(dinner), businessmeal(true), person(eugene).
drinkorder(redwine) :- context(dinner), companion(wife), person(eugene).
drinkorder(beer) :- context(dinner), companion(friend), person(eugene).

