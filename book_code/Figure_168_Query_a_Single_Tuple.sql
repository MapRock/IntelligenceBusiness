USE [AdventureWorksDW2017]
GO
--A single tuple. Figure 168.
SELECT
	PromotionKey,
	ProductKey,
	SUM(Freight) AS Freight
FROM
	[dbo].[FactInternetSales]
WHERE
	PromotionKey=1 AND ProductKey=361
GROUP BY
	PromotionKey,
	ProductKey
ORDER BY
	PromotionKey,
	ProductKey
