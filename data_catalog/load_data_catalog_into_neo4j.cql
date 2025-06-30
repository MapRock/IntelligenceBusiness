/*
Enterprise Intelligence - Supplemental Code

Author: Eugene Asahara
Book: Enterprise Intelligence
Publisher: Technics Publications

Copyright (c) 2024 Eugene Asahara. All rights reserved.

This file is part of the supplemental material for the book "Enterprise Intelligence".
It is provided "as-is" without any warranty, express or implied. The author and publisher
make no guarantees regarding the accuracy, completeness, or suitability of this code
for any particular purpose.

You are granted permission to use, modify, and distribute this code for personal,
educational, or commercial purposes, provided that this notice remains intact.

For more information, contact the publisher or eugene@softcodedlogic.com
*/

MATCH (n) DETACH DELETE n;


// Deleting existing nodes and relationships
MATCH (s:Server) DETACH DELETE s;
MATCH (c:Catalog) DETACH DELETE c;
MATCH (t:Table) DETACH DELETE t;
MATCH (col:Column) DETACH DELETE col;

// Importing data from CSV
//Created from sql_server_entire_server_data_catalog.sql
LOAD CSV WITH HEADERS FROM 'file:///sql_server_entire_server_data_catalog.csv' AS line
WITH line
WHERE line.ServerName IS NOT NULL 
AND line.Catalog IS NOT NULL 
AND line.TableName IS NOT NULL 
AND line.ColumnName IS NOT NULL

// Create/Merge Server node
MERGE (server:Server {label: line.ServerName})

// Create/Merge Catalog node with a combination of ServerName and Catalog for uniqueness
MERGE (catalog:Catalog {uniqueKey: line.ServerName + '-' + line.Catalog})
SET catalog.label = line.Catalog
MERGE (server)-[:HAS_CATALOG]->(catalog)

// Create/Merge Table node with a combination of ServerName, Catalog, and TableName for uniqueness
MERGE (table:Table {uniqueKey: line.ServerName + '-' + line.Catalog + '-' + line.TableName})
SET 
    table.label = line.TableName, 
    table.Table_Schema = line.TableSchema, 
    table.Table_Type = line.ObjectType,
    table.table_uri = line.table_uri,
    table.Description = CASE WHEN line.table_description IS NOT NULL THEN line.table_description ELSE NULL END

MERGE (catalog)-[:HAS_TABLE]->(table)

// Create/Merge Column node with a combination of ServerName, Catalog, TableName, and ColumnName for uniqueness
MERGE (column:Column {uniqueKey: line.ServerName + '-' + line.Catalog + '-' + line.TableName + '-' + line.ColumnName, label: line.ColumnName})
ON CREATE SET 
    column.type = line.ColumnType, 
    column.maxLength = toInteger(line.MaxLength), 
    column.isPrimaryKey = line.IsPrimaryKey,
    column.column_uri = line.column_uri,
    column.Description = CASE WHEN line.column_description IS NOT NULL THEN line.column_description ELSE NULL END

MERGE (table)-[:HAS_COLUMN]->(column)

// Link to ForeignKeyTable and ForeignKeyColumn only if they are not null
WITH column, line
WHERE line.ForeignKeyTable IS NOT NULL AND line.ForeignKeyColumn IS NOT NULL
MERGE (fkTable:Table {uniqueKey: line.ServerName + '-' + line.Catalog + '-' + line.ForeignKeyTable})
MERGE (fkColumn:Column {uniqueKey: line.ServerName + '-' + line.Catalog + '-' + line.ForeignKeyTable + '-' + line.ForeignKeyColumn})
MERGE (column)-[:REFERENCES]->(fkColumn)

// Use the Cypher query below to verify the data import.
// MATCH p=(c:Column)-[]-(t:Table)--(ct:Catalog) WHERE ct.label='MapRockSampleDatabase' AND t.Table_Schema='EARTHTRENDS' RETURN p