import sys
import os

# Add the src directory to the system path C:\MapRock\IntelligenceBusiness\src, where query_parse.py lives.
# This is assuming thi file is being run from C:\MapRock\IntelligenceBusiness\book_code
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

# Import the query_parse module
from query_parse import sql_hash as h

query = """
--This is a comment.
SELECT
    f.OrderDateKey / 100 AS [Month],
    SUM(f.TotalProductCost) AS Value2
FROM
    FactInternetSales f
    JOIN DimProduct p ON p.ProductKey = f.ProductKey --This is another comment.
WHERE
    f.ProductKey = 311  --Restrict to one product.
    AND f.SalesTerritoryKey IN (6, 7)
    AND f.OrderDateKey BETWEEN 20110101 AND 20111231
    AND p.ListPrice > 1000
GROUP BY
    f.OrderDateKey / 100
"""

print(h(query))
