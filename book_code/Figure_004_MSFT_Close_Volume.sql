USE Stocks
GO
 
SELECT 
    CAST(DateID AS DATE) AS [Date],
    Stock,
    [Close],
[Volume]
  FROM [dbo].[DailyFigures]
  WHERE DateID BETWEEN '2008-01-01' AND '2008-12-31'
    AND Stock IN ('MSFT')
ORDER BY [Date] ASC
