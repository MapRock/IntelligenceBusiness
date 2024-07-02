USE AdventureWorksDW2017
GO
--Both SQL include calculations involving common values: TaxAmt and OrderQuantity.
--The valuable information is that both calculations are affected by changes in either value.
SELECT
    c.EnglishEducation AS Education,
    SUM(
        (f.[SalesAmount] + f.[Freight] + f.[TaxAmt]) / f.[OrderQuantity]
    ) AS NetPerItem
FROM
    FactInternetSales f
    JOIN dbo.DimCustomer c ON c.CustomerKey = f.CustomerKey
GROUP BY
    c.EnglishEducation,
    f.[Freight] + f.[TaxAmt]
;
SELECT
    c.MaritalStatus,
    SUM(f.[TaxAmt] / f.[OrderQuantity]) AS TaxPerItem
FROM
    FactInternetSales f
    JOIN dbo.DimCustomer c ON c.CustomerKey = f.CustomerKey
GROUP BY
    c.MaritalStatus
