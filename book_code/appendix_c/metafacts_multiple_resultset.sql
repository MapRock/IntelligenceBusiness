USE [AdventureWorksDW2017]
GO

CREATE PROCEDURE [dbo].[usp_GetCustomerOrders]
AS
BEGIN
    -- First result set: Basic customer information
    SELECT TOP 10 CustomerKey, FirstName, LastName
    FROM DimCustomer WHERE CustomerKey BETWEEN 11000 AND 11010;

    -- Second result set: Basic order details
    SELECT TOP 10 CustomerKey, SalesOrderNumber, OrderDate, SalesAmount
    FROM FactInternetSales WHERE CustomerKey BETWEEN 11000 AND 11010;
END;