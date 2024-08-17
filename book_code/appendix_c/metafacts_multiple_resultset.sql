USE [AdventureWorksDW2017]
GO

CREATE PROCEDURE [dbo].[usp_GetCustomerOrders]
AS
BEGIN
    -- First result set: Basic customer information
    SELECT TOP 10 CustomerKey, FirstName, LastName
    FROM DimCustomer;

    -- Second result set: Basic order details
    SELECT TOP 10 SalesOrderNumber, OrderDate, SalesAmount
    FROM FactInternetSales;
END;