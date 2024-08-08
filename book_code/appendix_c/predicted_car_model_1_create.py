"""
This is the first of three Python programs demonstating the extraction of rules in a decision tree.

This is a simple program using sklearn's DecisionTreeClassifier to train a decision tree model on a sample dataset. 
The model is then saved to a pickle file.


After running this program, next two steps are:
1. Run the program predicted_car_model_2_read_dt_metadata.py to extract the rules from the decision tree model.
2. Run the program predicted_car_model_3_query.py to query the decision tree model.

"""
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import pickle

pickle_filename = 'c:\\temp\\car_model_predictor.pkl'

# Sample data
data = {
    'occupation': ['engineer', 'lawyer', 'farmer', 'engineer', 'lawyer', 'farmer'],
    'age': [55, 45, 25, 60, 35, 30],
    'car_model': ['Sedan', 'Sports', 'Truck', 'Sedan', 'Sports', 'Truck']
}

df = pd.DataFrame(data)

# Encoding categorical variables
df['occupation'] = df['occupation'].astype('category').cat.codes

# Features and target variable
X = df[['occupation', 'age']]
y = df['car_model']

# Train decision tree model
model = DecisionTreeClassifier()
model.fit(X, y)

# Save the model to a pickle file
with open(pickle_filename, 'wb') as file:
    pickle.dump(model, file)
