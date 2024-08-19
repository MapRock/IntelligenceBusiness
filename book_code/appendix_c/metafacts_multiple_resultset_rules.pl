% Rule to find customers who have made a purchase over a certain amount
high_value_customer(CustomerKey, FirstName, LastName, SalesAmount) :- 
        customer(CustomerKey, FirstName, LastName), 
        sales_order(CustomerKey, _, _, SalesAmount), 
        SalesAmount > 3380.

% Rule to check if a customer has multiple sales orders       
repeat_customer(CustomerKey, FirstName, LastName) :- 
        customer(CustomerKey, FirstName, LastName), 
        sales_order(CustomerKey, _, OrderDate1, _), 
        sales_order(CustomerKey, _, OrderDate2, _), 
        OrderDate1 \= OrderDate2.