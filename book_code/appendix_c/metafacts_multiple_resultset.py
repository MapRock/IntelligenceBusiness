import pyodbc
from pyswip import Prolog
import json
import datetime
import os

def load_config(config_file):
    """Load configuration from a JSON file and set the necessary variables."""
    with open(config_file, 'r') as f:
        config = json.load(f)
    return config["server"], config["database"], config["sql"], config["resultset_predicates"]

def connect_to_sql_server(server, database):
    """Establish a connection to the SQL Server database."""
    conn_str = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"Trusted_Connection=yes;"
    )
    return pyodbc.connect(conn_str)

def execute_stored_procedure(cursor, sql):
    """Execute the stored procedure and return the result sets."""
    cursor.execute(sql)
    return cursor

def process_result_sets(cursor, prolog, resultset_predicates):
    """Process each result set and assert Prolog facts."""
    result_count = 0
    predicates_list = list(resultset_predicates.keys())

    while True:
        try:
            columns = [column[0] for column in cursor.description]
            rows = cursor.fetchall()
            if rows:
                predicate = predicates_list[result_count]
                if not resultset_predicates[predicate]:
                    resultset_predicates[predicate] = columns
                column_order = resultset_predicates[predicate]
                assert_prolog_facts(prolog, rows, predicate, columns, column_order)
            
            if not cursor.nextset():
                break
            else:
                result_count += 1
        except pyodbc.ProgrammingError as e:
            print("Warning:", e)
            if not cursor.nextset():
                break

def assert_prolog_facts(prolog, rows, predicate, columns, column_order):
    """Assert Prolog facts based on the result set data."""
    for row in rows:
        values = [
            f"'{str(row[columns.index(col)])}'" if isinstance(row[columns.index(col)], (str, datetime.date, datetime.datetime)) else str(row[columns.index(col)])
            for col in column_order
        ]
        prolog_fact = f"{predicate}({', '.join(values)})"
        print(f"Asserting: {prolog_fact}")
        prolog.assertz(prolog_fact)

def query_prolog(prolog, resultset_predicates):
    """Query Prolog after all facts have been asserted."""
    for predicate in resultset_predicates:
        column_order = resultset_predicates[predicate]
        variables = ", ".join([col.capitalize() for col in column_order])
        prolog_query = f"{predicate}({variables})"
        print(f"\nExecuting query: {prolog_query}")
        for result in prolog.query(prolog_query):
            print(result)

if __name__ == "__main__":
    current_directory = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")

    config_file = f"{current_directory}/metafacts_multiple_resultset.json"
    #config_file = f"{current_directory}/metafacts.json" 

    # Load configuration and set variables
    server, database, sql, resultset_predicates = load_config(config_file)

    # Initialize Prolog
    prolog = Prolog()

    # Connect to SQL Server
    connection = connect_to_sql_server(server, database)
    cursor = connection.cursor()

    # Execute the stored procedure
    cursor = execute_stored_procedure(cursor, sql)

    # Process result sets and assert Prolog facts
    process_result_sets(cursor, prolog, resultset_predicates)

    # Close the database connection
    cursor.close()
    connection.close()

    # Query Prolog to verify
    query_prolog(prolog, resultset_predicates)
