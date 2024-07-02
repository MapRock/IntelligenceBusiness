USE [AdventureWorksDW2017]
GO
-- Drop the temporary table #s if it exists
DROP TABLE IF EXISTS #s;

-- Select and aggregate SalesAmount by OrderDateKey for SalesTerritoryKey = 9 and insert into #s
SELECT
    f.OrderDateKey/100 AS OrderDateKey,
    SUM(f.[SalesAmount]) AS [SalesAmount]
INTO #s
FROM
    FactInternetSales f
	JOIN [dbo].[DimCustomer] c ON c.CustomerKey = f.CustomerKey
WHERE
    f.OrderDateKey BETWEEN 20110101 AND 20111231
    AND c.MaritalStatus = 'M'
    AND f.[SalesTerritoryKey] = 9
GROUP BY
    f.OrderDateKey/100;

-- Drop the temporary table #p if it exists
DROP TABLE IF EXISTS #p;

-- Select and aggregate TotalProductCost by OrderDateKey for ProductKey = 311 in SalesTerritoryKeys 6 and 7, and insert into #p
SELECT
    f.OrderDateKey/100 AS OrderDateKey,
    SUM(f.[TotalProductCost]) AS [TotalProductCost]
INTO #p
FROM
    FactInternetSales f
JOIN
    DimProduct p ON p.ProductKey = f.ProductKey
WHERE
    f.[SalesTerritoryKey] IN (6, 7)
    AND f.OrderDateKey BETWEEN 20110101 AND 20111231
    AND p.ProductKey = 311
	AND p.ListPrice>1000
GROUP BY
    f.OrderDateKey/100;

-- Drop the temporary table #c if it exists
DROP TABLE IF EXISTS #c;

-- Join #s and #p on OrderDateKey, cast SalesAmount and TotalProductCost to float, and insert into #c
SELECT 
    s.OrderDateKey,
    CAST(s.SalesAmount AS float) AS SalesAmount,
    CAST(p.TotalProductCost AS float) AS TotalProductCost
INTO #c
FROM 
    #s s
JOIN 
    #p p ON s.OrderDateKey = p.OrderDateKey;

SELECT * FROM #c --Display the combined tables.

-- Drop the temporary table #averages if it exists
DROP TABLE IF EXISTS #averages;

-- Calculate the averages of SalesAmount and TotalProductCost and insert into #averages
SELECT
    AVG(SalesAmount) AS AvgSalesAmount,
    AVG(TotalProductCost) AS AvgTotalProductCost
INTO #averages
FROM 
    #c;

-- Calculate the Pearson correlation between SalesAmount and TotalProductCost using the data in #c and the averages in #averages
SELECT 
    (SUM((s.SalesAmount - a.AvgSalesAmount) * (s.TotalProductCost - a.AvgTotalProductCost)) /
    SQRT(SUM(POWER(s.SalesAmount - a.AvgSalesAmount, 2)) * SUM(POWER(s.TotalProductCost - a.AvgTotalProductCost, 2)))) AS PearsonCorrelation
FROM 
    #c s
	CROSS JOIN #averages a;
