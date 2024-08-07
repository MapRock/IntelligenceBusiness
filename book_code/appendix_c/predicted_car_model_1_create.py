import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import pickle

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
with open('c:\\temp\\car_model_predictor.pkl', 'wb') as file:
    pickle.dump(model, file)
