
// Create relationships indicating the effect of the from node increasing

MATCH 
(a:Problem {name: 'CPU Pressure'}), 
(b:Metric {name: 'Processor Time %'})
CREATE (a)-[:HAS_METRIC {description: 'An increase in Processor Time % indicates CPU pressure.'}]->(b);

MATCH 
(b:Metric {name: 'Processor Time %'}), 
(c:Metric {name: 'SQL Compilations/s'})
CREATE (b)-[:AFFECTS {description: 'Higher Processor Time % can be caused by frequent SQL Compilations.'}]->(c);

MATCH 
(a:Problem {name: 'Memory Pressure'}), 
(b:Metric {name: 'Page Life Expectancy'})
CREATE (a)-[:HAS_METRIC {description: 'Decrease in Page Life Expectancy suggests memory pressure.'}]->(b);

MATCH 
(b:Metric {name: 'Page Life Expectancy'}), 
(c:Metric {name: 'Buffer Cache Hit Ratio %'})
CREATE (b)-[:INFLUENCES {description: 'Lower Page Life Expectancy can decrease Buffer Cache Hit Ratio %.'}]->(c);

MATCH 
(c:Metric {name: 'Buffer Cache Hit Ratio %'}), 
(d:Metric {name: 'Page Reads/s'})
CREATE (c)-[:IMPACTS {description: 'Reduced Buffer Cache Hit Ratio % increases Page Reads from disk.'}]->(d);

MATCH 
(d:Metric {name: 'Page Reads/s'}), 
(e:Metric {name: 'Disk Queue Length'})
CREATE (d)-[:ELEVATES {description: 'More Page Reads/s can increase Disk Queue Length, suggesting I/O bottlenecks.'}]->(e);

MATCH 
(a:Problem {name: 'Network Latency'}), 
(b:Metric {name: 'Bytes Received/s'})
CREATE (a)-[:HAS_METRIC {description: 'Decrease in Bytes Received/s can hint at network latency issues.'}]->(b);

MATCH 
(a:Problem {name: 'Concurrency Issues'}), 
(b:Metric {name: 'Lock Waits/s'})
CREATE (a)-[:HAS_METRIC {description: 'A rise in Lock Waits/s indicates possible concurrency issues.'}]->(b);
