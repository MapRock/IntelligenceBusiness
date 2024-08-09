// Delete all relevant nodes (Patient, Symptom, Diagnosis) and their relationships
MATCH (n)
WHERE (n:Patient AND n.name IN ['John Doe', 'Jane Doe']) 
   OR (n:Symptom AND n.name = 'cough') 
   OR (n:Diagnosis AND n.name IN ['common_cold', 'emphysema', 'flu'])
DETACH DELETE n;

// Create Symptoms
CREATE (s1:Symptom {name: 'cough'})

// Create Diagnoses
CREATE (d1:Diagnosis {name: 'common_cold'})
CREATE (d2:Diagnosis {name: 'emphysema'})
CREATE (d3:Diagnosis {name: 'flu'})

// Create Patients
CREATE (p1:Patient {name: 'John Doe', age: 30, smokingStatus: 'non_smoker'})

// Create Relationships
CREATE (p1)-[:HAS_SYMPTOM {duration: '7 days'}]->(s1)
CREATE (p1)-[:HAS_DIAGNOSIS {probability_func: "common_cold_diagnosis_2.pl"}]->(d1)
CREATE (p1)-[:HAS_DIAGNOSIS {probability_func: "emphysema_diagnosis_2.pl"}]->(d2)
CREATE (p1)-[:HAS_DIAGNOSIS {probability_func: "flu_diagnosis_2.pl"}]->(d3)
