DROP TABLE IF EXISTS #BigChanges

CREATE TABLE #BigChanges (
    DateID date,
    Stock nvarchar(10),
    BigChange TINYINT
);

INSERT INTO #BigChanges (DateID, Stock, BigChange)
SELECT 
    DateID,
    Stock,
    CASE 
        WHEN ABS(( [Close] - LAG( [Close] ) OVER (PARTITION BY Stock ORDER BY DateID)) / LAG( [Close] ) OVER (PARTITION BY Stock ORDER BY DateID)) >= 0.01 THEN 1
        ELSE 0
    END AS BigChange
FROM 
    dbo.DailyFigures
WHERE 
    DateID BETWEEN '2022-06-01' AND '2023-06-30'
    AND Stock IN ('MSFT', 'INTC', 'GIS', 'AMD', 'JNJ', 'PFE', 'AMZN', 'NVDA');


DROP TABLE IF EXISTS #JointOccurrences

CREATE TABLE #JointOccurrences (
    StockA nvarchar(10),
    StockB nvarchar(10),
    CountA int,
    CountB int,
    CountAB int
);

INSERT INTO #JointOccurrences (StockA, StockB, CountA, CountB, CountAB)
SELECT 
    A.Stock AS StockA,
    B.Stock AS StockB,
    SUM(A.BigChange) AS CountA,
    SUM(B.BigChange) AS CountB,
    SUM(CASE WHEN A.BigChange = 1 AND B.BigChange = 1 THEN 1 ELSE 0 END) AS CountAB
FROM 
    #BigChanges A
JOIN 
    #BigChanges B ON A.DateID = B.DateID
WHERE 
    A.Stock != B.Stock
GROUP BY 
    A.Stock, B.Stock;

DROP TABLE IF EXISTS #ConditionalProbabilities

CREATE TABLE #ConditionalProbabilities (
    StockA nvarchar(10),
    StockB nvarchar(10),
	CountA INT,
	CountB INT,
	CountAB INT,
    P_A_given_B float,
    P_B_given_A float
);

INSERT INTO #ConditionalProbabilities (StockA, StockB, CountA, CountB,CountAB, P_A_given_B, P_B_given_A)
SELECT
    StockA,
    StockB,
	CountA,
	CountB,
	CountAB,
    CASE WHEN CountB > 0 THEN CAST(CountAB AS FLOAT) / CountB ELSE 0 END AS P_A_given_B,
    CASE WHEN CountA > 0 THEN CAST(CountAB AS FLOAT) / CountA ELSE 0 END AS P_B_given_A
FROM 
    #JointOccurrences;

select * from #ConditionalProbabilities