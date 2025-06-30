/*

sql_server_entire_data_catalog.sql

This will fetch metadata of a SQL Server instance and return a table. This table is the source for a Cypher
script, load_data_catalog_into_neo4j.cql, which will import this metadata into a Neo4j Data Catalog.

Prior to running this script, metadata obtained from Kyvos cubes are imported into [STAGE].[kyvos_trial_cluster]

Remember to set NULL (it's a string if we save it) as blank.

table_uri and column_uri are meant to link to the Knowledge Graph. It might be the tail wagging the dog in that
the KG authors should probably set the uri for tables and columns - not the data catalog setting the uri for the KG authors.
But I have this script setting a default of the ontology#table_name or ontology#column_name to illustrate the concept of
mapping the KG to the data catalog.
*/


DECLARE @DBName NVARCHAR(256)
DECLARE @SQL NVARCHAR(MAX)
DECLARE @ontology_prefix NVARCHAR(256) = 'http://www.example.org/ontology#'

DROP TABLE IF EXISTS #Results
-- Temporary table to hold the results
CREATE TABLE #Results (
    [ServerName] NVARCHAR(256),
    [Catalog] NVARCHAR(256), --Catalog, Database, Cube
	TableSchema NVARCHAR(256),
    TableName NVARCHAR(256),
    ColumnName NVARCHAR(256),
    ColumnType NVARCHAR(256),
    [MaxLength] INT NULL,
    ObjectType NVARCHAR(50),
    IsPrimaryKey NVARCHAR(10),
    ForeignKeyTable NVARCHAR(256) NULL,
    ForeignKeyColumn NVARCHAR(256) NULL,
	table_uri NVARCHAR(256) NULL, -- Tables and columns refer to objects, so they could have a uri.
	column_uri NVARCHAR(256) NULL,
	table_description NVARCHAR(256) NULL,
	column_description NVARCHAR(256) NULL
)

-- Get a list of databases from the SQL Server Instance.
DECLARE db_cursor CURSOR FOR
SELECT name 
FROM sys.databases 
WHERE database_id > 4 AND state_desc = 'ONLINE' -- excluding system databases

-- Looping through each user database in the SQL Server Instance.
OPEN db_cursor
FETCH NEXT FROM db_cursor INTO @DBName
WHILE @@FETCH_STATUS = 0
BEGIN
    SET @SQL = '
        USE [' + @DBName + ']

        INSERT INTO #Results
        SELECT 
            CONVERT(NVARCHAR(256), SERVERPROPERTY(''MachineName''))+CASE WHEN SERVERPROPERTY(''InstanceName'') IS NOT NULL THEN ''\'' + CONVERT(NVARCHAR(256), SERVERPROPERTY(''InstanceName'')) ELSE '''' END AS ServerName,
            ''' + @DBName + ''' AS Catalog,
			OBJECT_SCHEMA_NAME(c.object_id) AS TableSchema,
            OBJECT_NAME(c.object_id) AS TableName,
            c.name AS ColumnName,
            t.name AS ColumnType,
            c.max_length AS MaxLength,
            CASE WHEN OBJECTPROPERTY(c.object_id, ''IsView'') = 1 THEN ''View'' ELSE ''Base Table'' END AS ObjectType,
            CASE WHEN ic.key_ordinal IS NOT NULL THEN ''YES'' ELSE ''NO'' END AS IsPrimaryKey,
            OBJECT_NAME(fk.referenced_object_id) AS ForeignKeyTable,
            COL_NAME(fk.referenced_object_id, fk.referenced_column_id) AS ForeignKeyColumn,
			'''+@ontology_prefix+'''+OBJECT_NAME(c.object_id) AS table_uri,
			'''+@ontology_prefix+'''+c.name AS column_uri,
            CONVERT(NVARCHAR(256),ep.value) AS TableDescription,
            CONVERT(NVARCHAR(256),ep2.value) AS ColumnDescription
        FROM sys.columns c
			JOIN sys.types t ON c.system_type_id = t.system_type_id
			LEFT JOIN sys.index_columns ic ON ic.object_id = c.object_id AND ic.column_id = c.column_id AND ic.key_ordinal = 1
			LEFT JOIN sys.foreign_key_columns fk ON fk.parent_object_id = c.object_id AND fk.parent_column_id = c.column_id
			LEFT JOIN sys.extended_properties ep ON ep.major_id = c.object_id AND ep.minor_id = 0 AND ep.name = ''MS_Description'' -- Table descriptions
			LEFT JOIN sys.extended_properties ep2 ON ep2.major_id = c.object_id AND ep2.minor_id = c.column_id AND ep2.name = ''MS_Description'' -- Column descriptions
		WHERE 
			OBJECT_SCHEMA_NAME(c.object_id) <> ''sys'' AND t.name NOT IN (''sysname'')
    '
    EXEC sp_executesql @SQL
    FETCH NEXT FROM db_cursor INTO @DBName
END

CLOSE db_cursor
DEALLOCATE db_cursor

--Insert Kyvos Cubes
--Import flat file iowa_liquor_store_metadata_raw.csv into table named [STAGE].[iowa_liquor_store_metadata_raw]
--This is the actual Kyvos cluster, https://trial.kyvosinsights.com/kyvos/#/master/default

-- ** IMPORTANT NOTE **
-- The Catalog, TableName, and ColumnName is a little odd. This is because I used SQL for Kyvos and don't mention the dimension.
-- In SQL Server, the 'Catalog' is a database (a set of tables). In Kyvos, we'll call the 'Catalog' the folder, a set of cubes.
-- However, we skip the dimension. This is looking at a cube as a flattened one big table.

/*
--Might need to add datekey attributes.
  INSERT INTO [STAGE].[kyvos_trial_cluster]
	SELECT
		[cube],[dimension],[hierarchy],'datekey' AS [caption],[datatype],'[datekey]' AS [name],[role],[type],aggregation
	FROM 
		[STAGE].[kyvos_trial_cluster]
	WHERE
		[Caption]='Day' AND [dimension]='Date'
*/
DECLARE @KyvosDSN NVARCHAR(50)='YourDSN' --However, we use a DSN 'KyvosNew'.
DECLARE @KyvosCatalog NVARCHAR(50)='Your Kyvos Folder' -- This is the folder.
DECLARE @KyvosDatabase NVARCHAR(128)=(
		SELECT TOP 1 [Catalog] FROM #Results
		WHERE TableSchema = 'STAGE' AND TableName = 'kyvos_trial_cluster'
		)
IF @KyvosDatabase IS NOT NULL
    BEGIN
    SET @SQL = '
        USE [' + @KyvosDatabase + ']
		INSERT INTO #Results
			SELECT 
				'''+@KyvosDSN+''' AS ServerName,
				'''+@KyvosCatalog+''' AS [Catalog],
				NULL AS TableSchema, 
				[cube] AS TableName,
				REPLACE(REPLACE([Caption],''['',''''),'']'','''') AS ColumnName,
				datatype AS ColumnType,
				NULL AS [MaxLength],
				''Cube'' AS ObjectType,
				NULL AS IsPrimaryKey,
				NULL AS ForeignKeyTable,
				NULL AS ForeignKeyColumn,
				'''+@ontology_prefix+'[dimension]'' AS table_uri,
				'''+@ontology_prefix+'''+REPLACE(REPLACE([name],''['',''''),'']'','''') AS column_uri,
				NULL as table_description,
				NULL as column_description
			FROM
				['+@KyvosDatabase+'].[STAGE].kyvos_trial_cluster
		'
		print @sql
		EXEC sp_executesql @SQL
	END

/*
Retrieving results to display.
in the grid result, Copy with headers, paste in eugene_sql_database_catalog.csv in the neo4j import directory.
Remember to set NULL (it's a string if we save it) as blank.
This is the source for the Cypher script, load_data_catalog_into_neo4j.cql
*/
SELECT * FROM #Results
--where (ColumnName like '%Address%' or ColumnName like '%zip%' or ColumnName like '%state%') and TableName='S_Customer_HILTON_SERV_GUESTS'
	ORDER BY ServerName,[Catalog],TableSchema,TableName,[ColumnName]
/*
SET IDENTITY_INSERT [EventEnsemble].[dbo].[DimSources] ON;
TRUNCATE TABLE [EventEnsemble].[dbo].[DimSources]

INSERT INTO [EventEnsemble].[dbo].[DimSources]
	(SourceID,ServerName,[Catalog],TableSchema,TableName,ColumnName)
	SELECT DISTINCT
		ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS SourceID,
		ServerName AS ServerName,
		[Catalog],
		[TableSchema],
		TableName,
		ColumnName
	FROM
		#Results

SET IDENTITY_INSERT [EventEnsemble].[dbo].[DimSources] OFF;
*/

-- Clean up
DROP TABLE #Results
