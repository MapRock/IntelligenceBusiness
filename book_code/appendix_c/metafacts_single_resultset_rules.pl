% Define the rule for classifying a customer as high-risk
high_risk_customer(CustomerKey, FirstName, LastName) :-
   customer(CustomerKey, FirstName, LastName),
   credit_score(CustomerKey, Score), Score =< 600,
   annual_income(CustomerKey, Income), Income =< 50000.
credit_score(11009,800).
annual_income(11009,120000).
credit_score(11000,550).
annual_income(11000,45000).