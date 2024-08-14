
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
from sklearn.tree import DecisionTreeClassifier, export_text
import joblib
from pyswip import Prolog
import os

# Get the directory of the current script.
# Prolog needs / instead of \ in the path.
current_directory = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")

# Load the Iris dataset
iris = load_iris()

pkl_file = f'{current_directory}/decision_tree.pkl'
prolog_file = f'{current_directory}/iris_prolog_rules.pl'

clf = joblib.load(pkl_file)

feature_names = [name.replace(" ", "").replace("(", "").replace(")", "").capitalize() for name in iris.feature_names]
class_names = list(iris.target_names)

def generate_prolog_rules(tree, feature_names, class_names):
    rules = export_text(tree, feature_names=feature_names)
    print(rules)
    prolog_rules = []
    rule_stack = []
    operators = ["<=", ">=", "=", "!=", ">", "<"]

    for line in rules.split("\n"):
        depth = line.count("|   ")  # Calculate the depth based on the number of "|   " sequences
        stripped_line = line.replace("|---", "").replace("|   ", "").strip()

        if not stripped_line:
            continue

        # Adjust the rule stack based on the current depth
        if len(rule_stack) > depth:
            rule_stack = rule_stack[:depth]

        # Check if the line is a condition
        if any(op in stripped_line for op in operators):
            stripped_line = stripped_line.replace("<=", "=<")
            if rule_stack:
                rule_stack.append(f"{rule_stack[-1]}, {stripped_line}")
            else:
                rule_stack.append(stripped_line)
            continue

        # Check if the line is a class assignment (leaf node)
        if "class:" in stripped_line:
            class_idx = int(stripped_line.split("class:")[1])
            class_name = class_names[class_idx]

            # Get the index of the node
            node_index = len(prolog_rules)

            # Get the probability
            value = tree.tree_.value[node_index][0]
            total = sum(value)
            probability = value[class_idx] / total

            # Build the Prolog rule with underscores for unused features
            feature_string = ', '.join(
                feature if any(feature in cond for cond in rule_stack[-1].split(", ")) else "_" 
                for feature in feature_names
            )

            # Append the Prolog rule
            prolog_rules.append(f"p({feature_string}, {class_name}, {probability:.2f}) :- {rule_stack[-1]}.")

    return prolog_rules


# Usage example (assuming you have already trained a decision tree `clf`)
# Example features and target (this can be from any dataset)
# feature_names = ["SepalWidth", "SepalLength", "PetalWidth", "PetalLength"]
# class_names = ["setosa", "versicolor", "virginica"]

# Generate the Prolog rules
prolog_rules = generate_prolog_rules(clf, feature_names, class_names)

# Save the rules to a Prolog file
with open(prolog_file, 'w') as f:
    f.write(f"% pkl file name: {pkl_file}\n\n")
    f.write(":- dynamic p/6.\n\n")
    for rule in prolog_rules:
        f.write(f"{rule}\n")
