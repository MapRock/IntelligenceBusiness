from pyswip import Prolog
import os

def load_from_file(prolog, files: list):
    """Load facts into Prolog from text files, reading until a period to handle multi-line facts or rules."""
    for file_path in files:
        with open(file_path, 'r') as file:
            fact = ""
            for line in file:
                line = line.strip()
                
                # Ignore comments and empty lines
                if line.startswith('%') or not line:
                    continue

                # Accumulate lines into a single fact or rule until a period is found
                fact += " " + line
                if fact.endswith('.'):
                    # Remove the trailing period and assert the fact
                    prolog.assertz(fact.rstrip('.').strip())
                    fact = ""  # Reset for the next fact or rule

def test_query(prolog, query):
    """Run a query in Prolog and print the results."""
    print(f"Query: {query}")
    results = list(prolog.query(query))
    for result in results:
        print(result)
    if not results:
        print("No results found.")

if __name__ == "__main__":
    current_directory = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")

    prolog = Prolog()
    files = [
        f"{current_directory}/metafacts_multiple_resultset.pl",
        f"{current_directory}/metafacts_multiple_resultset_rules.pl"
    ]
    load_from_file(prolog, files)

    # Additional sale for 11006 so we have a repeat customer.
    prolog.assertz("sales_order(11006, 'SO43819a', '2011-01-25 00:00:00', 3399.9900)")

    # Test queries
    test_query(prolog, "high_value_customer(CustomerKey, FirstName, LastName, SalesAmount)")
    test_query(prolog, "repeat_customer(CustomerKey, FirstName, LastName)")
