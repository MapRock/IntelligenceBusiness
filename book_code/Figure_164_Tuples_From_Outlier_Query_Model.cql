//Figure 164. Two tuples from an Outlier Model of a Query.
MATCH (t1:Tuple)-[:MEMBER_OF]-(m1:Member {label: "313.0"}),
      (t2:Tuple)-[:MEMBER_OF]-(m2:Member {label: "312.0"})
MATCH (t1)-[:MEASURE_OF]-(meas1:Column {label: "TotalProductCost"}),
      (t2)-[:MEASURE_OF]-(meas2:Column {label: "TotalProductCost"})
MATCH (t2)-[:OF_MODEL]-(mdl1:Model {label: "Outliers"})-[:MODEL_OF]-(q:QueryDef)
RETURN *