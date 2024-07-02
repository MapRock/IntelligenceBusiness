
// Creating nodes for the main entities
CREATE (toothpaste:Substance {name: 'Toothpaste with Fluoride', description: 'A dental hygiene substance containing fluoride to prevent cavities.'})
CREATE (bacteria:Agent {name: 'Bacteria', description: 'Microorganisms in the mouth that convert sugars into acids.'})
CREATE (acid:Substance {name: 'Acids', description: 'Substances produced by bacteria from sugars that can demineralize tooth enamel.'})
CREATE (fluorapatite:Substance {name: 'Fluorapatite', description: 'An acid-resistant material formed on tooth enamel in the presence of fluoride.'})
CREATE (remineralization:Process {name: 'Remineralization', description: 'The process where minerals are redeposited into tooth enamel after being removed by acids.'})

// Creating relationships between the nodes
CREATE (toothpaste)-[:INHIBITS {description: 'Fluoride in toothpaste inhibits'}]->(bacteria)
CREATE (bacteria)-[:PRODUCES {description: 'Bacteria feed on sugars producing'}]->(acid)
CREATE (toothpaste)-[:PROMOTES {description: 'Fluoride in toothpaste promotes'}]->(remineralization)
CREATE (acid)-[:ATTACKS {description: 'Acids attack and can demineralize'}]->(remineralization)
CREATE (toothpaste)-[:LEADS_TO_FORMATION {description: 'Fluoride in toothpaste leads to the formation of'}]->(fluorapatite)
