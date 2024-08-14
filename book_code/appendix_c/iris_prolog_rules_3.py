from pyswip import Prolog

# Initialize Prolog
prolog = Prolog()

# Load the Prolog rules generated from the decision tree
prolog.consult("c:/temp/iris_prolog_rules.pl")
prolog.consult("C:/MapRock/IntelligenceBusiness/book_code/appendix_c/iris_prolog_rules_action.pl")

# Execute a query to classify the same iris flower based on its features using Prolog
list(prolog.query("send_if_virginica(5.8, 2.7, 5.1, 1.9)."))
