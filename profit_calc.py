import json

# Load the output.json data
with open('output.json', 'r') as json_file:
    data = json.load(json_file)

# Extract location, crop, soil PH, and Temperature
location = data.get("location", "")
crop = data.get("crop", "")
soil_ph = data.get("soil PH", "")
temperature = data.get("Temperature", "")

# Extract the first number from "soil PH" (assuming it's in the format "7.5-8.0")
soil_ph_first_value = soil_ph.split('-')[0] if soil_ph else ""

# Remove '°C' from the Temperature string to keep only the numeric values
temperature_value = temperature.replace("°C", "") if temperature else ""

# Prepare the output with all the necessary fields
output_data = {
    
    "crop": crop,
    "soil PH": soil_ph_first_value,
    "Temperature": temperature_value
}

# Print the output (or you can further process or save it)
print(f"Processed Data: {json.dumps(output_data, indent=4)}")
