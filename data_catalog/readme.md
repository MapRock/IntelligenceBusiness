<!DOCTYPE html>
<html lang="en">

<body>
  <h1>SQL Server Entire Server Data Catalog → Neo4j</h1>

  <p>
    This code in this directory extracts metadata from every database, table, and column in your SQL Server instance,
    exports it to CSV, and then ingests it into Neo4j to build a browsable graph of your enterprise data catalog.
  </p>

  <h2>Prerequisites</h2>
  <ul>
    <li>Microsoft SQL Server &amp; SQL Server Management Studio (SSMS)</li>
    <li>Neo4j (Community or Enterprise)</li>
    <li>Write privileges in the Neo4j <code>import</code> directory</li>
  </ul>

  <h2>1. Export Metadata from SQL Server</h2>
  <p>
    In SSMS, run the <code>sql_server_entire_server_data_catalog.sql</code> script. It queries
    <code>sys.databases</code>, <code>sys.schemas</code>, <code>sys.tables</code>, and
    <code>sys.columns</code> across all user databases, and produces a flat result set of:
  </p>
  <ul>
    <li><strong>DatabaseName</strong></li>
    <li><strong>SchemaName</strong></li>
    <li><strong>TableName</strong></li>
    <li><strong>ColumnName</strong></li>
    <li><strong>DataType</strong></li>
    <li>Additional metadata (max length, precision, nullable, etc.)</li>
  </ul>
  <p>
    Save the results as CSV named:
  </p>
  <pre><code>sql_server_entire_server_data_catalog.csv</code></pre>
  <p>
    Place this file into your Neo4j <code>import</code> directory.
  </p>

  <h2>2. Load into Neo4j</h2>
  <p>
    Use the CQL script <code>load_data_catalog_into_neo4j.cql</code> to ingest the CSV into your graph.
    It should include a statement like:
  </p>
  <pre><code>
LOAD CSV WITH HEADERS
  FROM 'file:///sql_server_entire_server_data_catalog.csv'
  AS line
MERGE (db:Database { name: line.DatabaseName })
MERGE (sch:Schema { name: line.SchemaName })
  ON CREATE SET sch.database = line.DatabaseName
MERGE (tbl:Table   { name: line.TableName, schema: line.SchemaName })
  ON CREATE SET tbl.database = line.DatabaseName
MERGE (col:Column  { name: line.ColumnName })
  ON CREATE SET
    col.table       = line.TableName,
    col.schema      = line.SchemaName,
    col.database    = line.DatabaseName,
    col.data_type   = line.DataType,
    col.max_length  = line.MaxLength,
    col.is_nullable = line.IsNullable
MERGE (db)-[:HAS_SCHEMA]->(sch)
MERGE (sch)-[:HAS_TABLE]->(tbl)
MERGE (tbl)-[:HAS_COLUMN]->(col);
  </code></pre>

  <h2>3. Resulting Graph Model</h2>
  <ul>
    <li><strong>(Database)</strong> nodes, keyed by <code>name</code>.</li>
    <li><strong>(Schema)</strong> nodes, keyed by <code>name</code>, with a <code>database</code> property.</li>
    <li><strong>(Table)</strong> nodes, keyed by <code>name</code>, with <code>schema</code> and <code>database</code> properties.</li>
    <li><strong>(Column)</strong> nodes, keyed by <code>name</code>, with <code>table</code>, <code>schema</code>, <code>database</code>, <code>data_type</code>, etc.</li>
    <li>Relationships:
      <ul>
        <li><code>(Database)-[:HAS_SCHEMA]->(Schema)</code></li>
        <li><code>(Schema)-[:HAS_TABLE]->(Table)</code></li>
        <li><code>(Table)-[:HAS_COLUMN]->(Column)</code></li>
      </ul>
    </li>
  </ul>

  <h2>4. Usage</h2>
  <ol>
    <li>Run <code>sql_server_entire_server_data_catalog.sql</code> in SSMS.</li>
    <li>Save to CSV and move to <code>import/</code> in your Neo4j home.</li>
    <li>Open the CSV and replace the string NULL with a blank.
    <li>Start Neo4j and execute <code>load_data_catalog_into_neo4j.cql</code> from the Browser or Cypher shell. Warning: Be sure to use a Neo4j database dedicated to the tutorial.</li>
    <li>Explore your new <em>Data Catalog Graph</em>!</li>
  </ol>

  <hr>
  <p><em>Generated on June 30, 2025</em></p>
</body>
</html>
