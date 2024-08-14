from pyswip import Prolog
import os

# Get the directory of the current script.
# Prolog needs / instead of \ in the path.
current_directory = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")

# Initialize Prolog
prolog = Prolog()

# Load the Prolog rules generated from the decision tree
prolog.consult(f"{current_directory}/iris_prolog_rules_action.pl")

# Execute a query to classify the same iris flower based on its features using Prolog
list(prolog.query("send_if_iris_found(5.8, 2.7, 5.1, 1.9).")) # Virginica, 1.00
list(prolog.query("send_if_iris_found(5.8, 2.7, 5.1, 1.6).")) # Versicolor, 0.98

