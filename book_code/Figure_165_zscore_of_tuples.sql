USE AdventureWorksDW2017
GO
-- Calculate the averages and standard deviations
WITH [Stats] AS (
    SELECT
        AVG(TotalProductCost) AS AvgTotalProductCost,
        STDEV(TotalProductCost) AS StdDevTotalProductCost,
        AVG(SalesAmount) AS AvgSalesAmount,
        STDEV(SalesAmount) AS StdDevSalesAmount
    FROM (
        SELECT
            SUM(f.[SalesAmount]) AS SalesAmount,
            SUM(f.[TotalProductCost]) AS TotalProductCost,
            f.[ProductKey]
        FROM
            FactInternetSales f
        WHERE
            f.[SalesTerritoryKey] IN (6, 7)
        GROUP BY
            f.[ProductKey]
    ) AS Aggregated
),

-- Calculate the z-scores
ZScores AS (
    SELECT
        f.[ProductKey],
        SUM(f.[SalesAmount]) AS SalesAmount,
        SUM(f.[TotalProductCost]) AS TotalProductCost,
        (SUM(f.[TotalProductCost]) - [Stats].AvgTotalProductCost) / Stats.StdDevTotalProductCost AS product_cost_zscore,
        (SUM(f.[SalesAmount]) - [Stats].AvgSalesAmount) / Stats.StdDevSalesAmount AS sales_amount_zscore
    FROM
        FactInternetSales f,
        Stats
    WHERE
        f.[SalesTerritoryKey] IN (6, 7)
    GROUP BY
        f.[ProductKey], Stats.AvgTotalProductCost, Stats.StdDevTotalProductCost, Stats.AvgSalesAmount, Stats.StdDevSalesAmount
)

-- Final select to display results
SELECT
    ProductKey,
    SalesAmount,
    TotalProductCost,
    product_cost_zscore,
    sales_amount_zscore
FROM
    ZScores
ORDER BY
    product_cost_zscore DESC
