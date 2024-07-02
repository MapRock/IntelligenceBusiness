MATCH (q)-[:FILTER_OF]-(f:Filter)--(s:Set)
MATCH (q)-[:DICED_BY]-(c:Column) WHERE c.label IN ["ProductKey", "PromotionKey"]
MATCH (s)-[:OF_SET]-(m1:Member {label: "6"})
MATCH (s)-[:OF_SET]-(m2:Member {label: "7"})
RETURN *