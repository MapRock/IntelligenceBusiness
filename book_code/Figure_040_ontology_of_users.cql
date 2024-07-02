
// Create users and their associated metadata

// User: Eva
CREATE (eva:User {name: ‘Eva'})
MERGE (skill1:Skill {name: 'Data Visualization'})
MERGE (skill2:Skill {name: 'Statistics'})
MERGE (role1:Role {name: 'Software Engineer'})
MERGE (title1:Title {name: 'Senior Project Manager'})
MERGE (dept1:Department {name: 'IT'})
MERGE (eva)-[:HAS_SKILL]->(skill1)
MERGE (eva)-[:HAS_SKILL]->(skill2)
MERGE (eva)-[:HAS_ROLE]->(role1)
MERGE (eva)-[:HAS_TITLE]->(title1)
MERGE (eva)-[:BELONGS_TO]->(dept1);

// User: curt
CREATE (curt:User {name: 'curt'})
MERGE (skill3:Skill {name: 'Customer Relationship Management (CRM)'})
MERGE (skill4:Skill {name: 'Data Engineering'})
MERGE (role2:Role {name: 'Analyst'})
MERGE (title2:Title {name: 'Project Manager'})
MERGE (dept2:Department {name: 'Sales'})
MERGE (curt)-[:HAS_SKILL]->(skill1)  // Note: curt shares the 'Data Visualization' skill with eva
MERGE (curt)-[:HAS_SKILL]->(skill3)
MERGE (curt)-[:HAS_SKILL]->(skill4)
MERGE (curt)-[:HAS_ROLE]->(role2)
MERGE (curt)-[:HAS_TITLE]->(title2)
MERGE (curt)-[:BELONGS_TO]->(dept2);

// User: sally
CREATE (sally:User {name: 'sally'})
MERGE (skill5:Skill {name: 'Project Management'})
MERGE (skill6:Skill {name: 'Logistics'})
MERGE (role3:Role {name: 'Operations'})
MERGE (title3:Title {name: 'Project Manager'}) // Note: sally shares the 'Project Manager' title with curt
MERGE (dept3:Department {name: 'Logistics'})
MERGE (sally)-[:HAS_SKILL]->(skill5)
MERGE (sally)-[:HAS_SKILL]->(skill6)
MERGE (sally)-[:HAS_ROLE]->(role3)
MERGE (sally)-[:HAS_TITLE]->(title3)
MERGE (sally)-[:BELONGS_TO]->(dept3);
