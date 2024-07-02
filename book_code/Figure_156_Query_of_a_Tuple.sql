USE AdventureWorksDW2017
GO

SELECT
    ProductKey,
    SalesTerritoryKey,
    PromotionKey,
    MAX(SalesAmount) AS SalesAmount
FROM
    [dbo].[FactInternetSales]
WHERE
    ProductKey = 313
    AND SalesTerritoryKey = 6
    AND PromotionKey = 1
    AND OrderDateKey BETWEEN 20110101 AND 20111231
GROUP BY
    ProductKey,
    SalesTerritoryKey,
    PromotionKey
