//Figure 152.
//QueryDef description is: 	SALESAMOUNT of SalesAmount by SalesTerritoryKey filtered by OrderDateKey is between 20110101 AND 20111231 AND MaritalStatus = M
//Click on the QueryDef node to see the properties.
MATCH p=(m:Column{label:"MaritalStatus"})--(n:Member)<-[]-(f)-[]->(q:QueryDef) 
WHERE n.label STARTS WITH "M" 
RETURN p LIMIT 250            
