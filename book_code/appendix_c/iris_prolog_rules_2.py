
"""
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

For more information, visit the book's official page or contact the publisher.
"""
from sklearn.datasets import load_iris
import joblib
from pyswip import Prolog
import os

# Get the directory of the current script.
# Prolog needs / instead of \ in the path.
current_directory = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")


iris = load_iris()

# Load the trained Decision Tree model from the pickle file
pkl_file = f"{current_directory}/decision_tree.pkl"

loaded_model = joblib.load(pkl_file)

# Define the input features for testing (same as those used in the Prolog query)
input_features = [[1.0, 4.5, 5.0, 5.5]]

# Predict the class using the loaded model
predicted_class_index = loaded_model.predict(input_features)[0]
# predicted_class_name = iris.target_names[predicted_class_index]
predicted_probabilities = loaded_model.predict_proba(input_features)[0]
print(f"Probabilities for each class: {dict(zip(iris.target_names, predicted_probabilities))}")

# Initialize Prolog
prolog = Prolog()

# Load the Prolog rules generated from the decision tree
prolog.consult(f"{current_directory}/iris_prolog_rules.pl")

# Execute a query to classify the same iris flower based on its features using Prolog
# Create the query string dynamically using join
query_string = f"p({', '.join(str(a) for a in input_features[0] )}, Guess, Probability)"
print(query_string)
query = list(prolog.query(query_string))

# Print the results from Prolog
for result in query:
    print(f"Prolog Guess: {result['Guess']}, Probability: {result['Probability']}")