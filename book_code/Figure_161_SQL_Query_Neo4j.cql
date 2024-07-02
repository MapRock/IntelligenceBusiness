MATCH (q:QueryDef)
MATCH (q)<-[:DICED_BY]-(column1:Column)<--(table1:Table)
MATCH (q)<-[:FILTER_OF]-(f2:Filter)--(mf:Member)--(column2:Column)<--(table2:Table) WHERE mf.label="M"
MATCH (q)<-[:FILTER_OF]-(f3:Filter)--(s3:Set)--(m3:Member)--(column3:Column)<--(table3:Table)
MATCH (q)<-[:MEASURE_OF]-(column4:Column)<--(table4:Table)
MATCH (q)<-[:MODEL_OF]-(mdl4:Model)
RETURN *