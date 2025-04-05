import requests
import re

def ask_ollama_for_soil_data(location: str) -> dict:
    # Define prompts for both soil pH and soil moisture
    pH_prompt = f"What is the soil pH in {location} in India?"
    moisture_prompt = f"What is the soil moisture in {location} in India?"

    try:
        # Send request for soil pH
        pH_response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "llama2", "prompt": pH_prompt, "stream": False},
            timeout=2000
        )
        # Send request for soil moisture
        moisture_response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "llama2", "prompt": moisture_prompt, "stream": False},
            timeout=2000
        )

        # Check if both requests were successful
        if pH_response.status_code == 200 and moisture_response.status_code == 200:
            pH_full_text = pH_response.json().get("response", "").strip()
            moisture_full_text = moisture_response.json().get("response", "").strip()

            # Extract soil pH using regex
            pH_match = re.search(r"(\d+(\.\d+)?\s*(to|-)\s*\d+(\.\d+)?)|\d+(\.\d+)?", pH_full_text)
            soil_ph = pH_match.group(0) if pH_match else pH_full_text

            # Extract soil moisture using regex
            moisture_match = re.search(r"\d+(\.\d+)?", moisture_full_text)
            soil_moisture = moisture_match.group(0) if moisture_match else moisture_full_text

            # Return both pH and moisture as a dictionary
            return {
                "soil_ph": soil_ph,
                "soil_moisture": soil_moisture
            }
        else:
            return {
                "error": f"Ollama error: {pH_response.status_code} - {pH_response.text} (pH) or {moisture_response.status_code} - {moisture_response.text} (moisture)"
            }
    except Exception as e:
        return {
            "error": f"Exception: {str(e)}"
        }
