// Creating nodes for roles
CREATE (:Role {name: 'Dentist', specialty: 'General Dentistry', credentials: 'DDS', tasks: ['Examining teeth', 'Performing procedures']});
CREATE (:Role {name: 'Dentist', specialty: 'Orthodontics', credentials: 'DDS', tasks: ['Applying braces', 'Adjusting braces']});
CREATE (:Role {name: 'Hygienist', credentials: 'RDH', tasks: ['Cleaning teeth', 'Taking x-rays']});
CREATE (:Role {name: 'Assistant', credentials: 'CDA', tasks: ['Assisting in procedures', 'Sterilizing instruments']});
CREATE (:Role {name: 'Receptionist', tasks: ['Scheduling appointments', 'Managing patient records']});

// Creating nodes for visit and appointment
CREATE (:Visit {id: 'V001', date: '2024-06-01', patient: 'John Doe'});
CREATE (:Appointment {id: 'A001', visitId: 'V001', type: 'Dental Checkup', date: '2024-06-01'});

// Creating nodes for procedures
CREATE (:Procedure {code: 'D1110', name: 'Prophylaxis', description: 'Cleaning of teeth', duration: '30 minutes'});
CREATE (:Procedure {code: 'D8080', name: 'Comprehensive Orthodontic Treatment', description: 'Application and adjustment of braces', duration: '1 hour'});

// Relating roles to humans (example humans)
CREATE (:Human {name: 'Dr. Smith', role: 'Dentist'});
CREATE (:Human {name: 'Alice Johnson', role: 'Hygienist'});

// Creating relationships
MATCH (r:Role {name: 'Dentist', specialty: 'General Dentistry'}), (h:Human {name: 'Dr. Smith'})
CREATE (h)-[:HAS_ROLE]->(r);

MATCH (r:Role {name: 'Hygienist'}), (h:Human {name: 'Alice Johnson'})
CREATE (h)-[:HAS_ROLE]->(r);

MATCH (v:Visit {id: 'V001'}), (a:Appointment {id: 'A001'})
CREATE (v)-[:INCLUDES]->(a);

MATCH (v:Visit {id: 'V001'}), (p:Procedure {code: 'D1110'})
CREATE (v)-[:INCLUDES]->(p);

MATCH (v:Visit {id: 'V001'}), (p:Procedure {code: 'D8080'})
CREATE (v)-[:INCLUDES]->(p);

// Relating appointment to visit
MATCH (a:Appointment {id: 'A001'}), (v:Visit {id: 'V001'})
CREATE (a)-[:PART_OF]->(v);

// Relating procedures to roles
MATCH (r:Role {name: 'Dentist', specialty: 'General Dentistry'}), (p:Procedure {code: 'D1110'})
CREATE (r)-[:PERFORMS]->(p);

MATCH (r:Role {name: 'Dentist', specialty: 'Orthodontics'}), (p:Procedure {code: 'D8080'})
CREATE (r)-[:PERFORMS]->(p);
