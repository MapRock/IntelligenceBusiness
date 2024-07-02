USE Stocks
GO

WITH StockPrices AS (
    SELECT 
        DateID,
        MAX(CASE WHEN Stock = 'MSFT' THEN [Close] END) AS MSFT,
        MAX(CASE WHEN Stock = 'NVDA' THEN [Close] END) AS NVDA,
        RANK() OVER (ORDER BY DateID) AS rnk
    FROM
        [dbo].[DailyFigures]
    WHERE
        Stock IN ('MSFT', 'NVDA') AND
        DateID BETWEEN '2022-07-25' AND '2023-07-24'
    GROUP BY
        DateID
)
SELECT
    sp.DateID,
    sp.MSFT,
    sp.NVDA,
    CASE 
        WHEN sp_prev.MSFT IS NULL THEN NULL
        ELSE (sp.MSFT - sp_prev.MSFT) / sp_prev.MSFT * 100
    END AS MSFT_dod, 
    CASE 
        WHEN sp_prev.NVDA IS NULL THEN NULL
        ELSE (sp.NVDA - sp_prev.NVDA) / sp_prev.NVDA * 100
    END AS NVDA_dod
FROM
    StockPrices sp
LEFT JOIN
    StockPrices sp_prev
ON
    sp.rnk = sp_prev.rnk + 1
ORDER BY
    sp.DateID;


--Get the Pearson Correlation between MSFT and NVDA. Sorry it's so involved.
WITH StockPrices AS (
    SELECT 
        DateID,
        MAX(CASE WHEN Stock = 'MSFT' THEN [Close] END) AS MSFT,
        MAX(CASE WHEN Stock = 'NVDA' THEN [Close] END) AS NVDA
    FROM
        [dbo].[DailyFigures]
    WHERE
        Stock IN ('MSFT', 'NVDA') AND
        DateID BETWEEN '2022-07-25' AND '2023-07-24'
    GROUP BY
        DateID
),
Averages AS (
    SELECT
        AVG(MSFT) AS AvgMSFT,
        AVG(NVDA) AS AvgNVDA
    FROM
        StockPrices
),
Deviations AS (
    SELECT
        SP.DateID,
        SP.MSFT,
        SP.NVDA,
        SP.MSFT - A.AvgMSFT AS DevMSFT,
        SP.NVDA - A.AvgNVDA AS DevNVDA
    FROM
        StockPrices SP
    CROSS JOIN
        Averages A
),
DeviationsSquared AS (
    SELECT
        DevMSFT * DevNVDA AS CovarianceTerm,
        POWER(DevMSFT, 2) AS DevMSFTSquared,
        POWER(DevNVDA, 2) AS DevNVDASquared
    FROM
        Deviations
)
SELECT
    SUM(CovarianceTerm) /
    (SQRT(SUM(DevMSFTSquared)) * SQRT(SUM(DevNVDASquared))) AS PearsonCorrelation
FROM
    DeviationsSquared;
