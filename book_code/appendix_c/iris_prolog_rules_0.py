
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
X, y = iris.data, iris.target

# Train a Decision Tree classifier
clf = DecisionTreeClassifier(random_state=42)
clf.fit(X, y)

pkl_file = f'{current_directory}/decision_tree.pkl'

# Save the model as a .pkl file
joblib.dump(clf, pkl_file)