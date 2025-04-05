import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
import json
import requests
import re

# Market price predictor function
def market_price_predictor(json_input):
    # Load the dataset from CSV
    data = pd.read_csv('merged_farm_market_summary.csv')

    # Define features and target
    features = ['Soil_pH', 'Soil_Moisture', 'Temperature_C', 'Crop_Type']
    target = 'Market_Price_per_ton'

    # Handle categorical variables
    preprocessor = ColumnTransformer(
        transformers=[
            ('crop', OneHotEncoder(handle_unknown='ignore'), ['Crop_Type'])
        ],
        remainder='passthrough')

    # Prepare the data
    X = data[features]
    y = data[target]

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Preprocess the training and testing data
    X_train = preprocessor.fit_transform(X_train)
    X_test = preprocessor.transform(X_test)

    # Train the Random Forest model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Parse JSON data
    input_data = json.loads(json_input)

    # Create a DataFrame from input features
    input_df = pd.DataFrame([input_data])

    # Ensure the order of columns matches the training data
    input_df = input_df[['Soil_pH', 'Soil_Moisture', 'Temperature_C', 'Crop_Type']]

    # Preprocess the input data
    input_processed = preprocessor.transform(input_df)

    # Predict the market price
    predicted_price = model.predict(input_processed)
    return predicted_price[0]

# Function to process the output JSON and retrieve relevant fields
def process_output_json(file_path):
    try:
        # Load and process data from output.json
        with open(file_path, 'r') as file:
            data = json.load(file)

        # Extract and process values
        soil_ph = data.get('soil PH', None)
        temperature = data.get('Temperature', 'Not available')
        temperature = temperature.replace('°C', '').strip()

        soil_moisture = data.get('soil moisture', 'Not available')  # Assuming this field exists
        crop = data.get('Crop', 'Not specified')  # Assuming this field exists

        # Prepare input for market prediction
        input_data = {
            "Soil_pH": soil_ph,
            "Soil_Moisture": soil_moisture,
            "Temperature_C": temperature,
            "Crop_Type": crop
        }

        return input_data

    except Exception as e:
        return {"error": f"Exception occurred: {str(e)}"}

# Function to query Ollama for farming advice
def ask_ollama_for_farming_advice(input_data: dict) -> dict:
    # Define the prompt for farming advice
    ollama_prompt = f"Given the following information:\nSoil PH: {input_data['Soil_pH']}\nTemperature: {input_data['Temperature_C']}°C\nSoil Moisture: {input_data['Soil_Moisture']}\nCrop: {input_data['Crop_Type']}\nPlease provide farming advice on how to improve the soil, optimize crop yield, and adapt to the weather."

    try:
        # Send request for farming advice
        response = requests.post(
            "http://localhost:11434/api/generate",  # Replace with your local API endpoint if different
            json={"model": "llama2", "prompt": ollama_prompt, "stream": False},
            timeout=2000
        )

        # Check if the request was successful
        if response.status_code == 200:
            response_data = response.json()
            farming_advice = response_data.get("response", "No advice provided.")
            return {
                "farming_advice": farming_advice
            }
        else:
            return {
                "error": f"Ollama error: {response.status_code} - {response.text}"
            }

    except Exception as e:
        return {
            "error": f"Exception: {str(e)}"
        }

# Main execution: process input data and get predictions and advice
def main():
    input_data = process_output_json('output.json')  # Assuming 'output.json' contains relevant farm data
    if "error" in input_data:
        print(input_data["error"])
    else:
        # Convert the input data to JSON format
        json_input = json.dumps(input_data)

        # Predict the market price using the market_price_predictor function
        predicted_price = market_price_predictor(json_input)

        # Print the processed values and predicted market price
        print(f"Soil PH: {input_data['Soil_pH']}")
        print(f"Temperature: {input_data['Temperature_C']}")
        print(f"Soil Moisture: {input_data['Soil_Moisture']}")
        print(f"Crop: {input_data['Crop_Type']}")
        print(f"Predicted Market Price for this input: {predicted_price}")

        # Query Ollama for farming advice
        farming_advice = ask_ollama_for_farming_advice(input_data)
        '''if "farming_advice" in farming_advice:
            print("\nFarming Advice:")
            print(farming_advice["farming_advice"])
        else:
            print(farming_advice["error"])'''
        print(farming_advice)
# Run the main function
if __name__ == "__main__":
    main()
