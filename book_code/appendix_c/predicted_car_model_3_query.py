import joblib
import pandas as pd
from sklearn.preprocessing import LabelEncoder

pickle_filename = 'c:\\temp\\car_model_predictor.pkl'


def predict_car_model(age, occupation):
    # Load the trained model
    model = joblib.load(pickle_filename)

    # Label encoder for the occupation feature
    label_encoder = LabelEncoder()
    
    # Fit the encoder on the training data categories (this should be done during training and saved)
    label_encoder.fit(['engineer', 'doctor', 'teacher', 'lawyer', 'farmer'])

    # Prepare input data with matching feature names
    input_data = {
        'occupation': occupation,
        'age': age
    }
    input_df = pd.DataFrame([input_data])

    # Transform input data
    input_df['occupation'] = label_encoder.transform(input_df['occupation'])

    # Reorder columns to match the training order
    input_df = input_df[['occupation', 'age']]

    # Make the prediction
    predicted_car_type = model.predict(input_df)

    return predicted_car_type[0]

# Example usage
if __name__ == "__main__":
    age = 30
    occupation = "engineer"
    predicted_car_model = predict_car_model(age, occupation)
    if predicted_car_model:
        print(f"Predicted car model: {predicted_car_model}")
