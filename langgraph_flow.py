from fastapi import FastAPI, HTTPException
import json
from backend.agents.farmer_advisor import get_farm_advice
from backend.agents.market_researcher import get_market_data
from backend.agents.weather_agent import get_weather_data
from backend.agents.environment_agent import ask_ollama_for_soil_data  # Adjusted to the new function

app = FastAPI()

@app.post("/run-agents")
def run_ai_agents(input_data: dict):
    try:
        location = input_data.get("location", "Delhi")
        crop = input_data.get("crop", "Wheat")

        # Get market data based on the crop (no await, as it's synchronous now)
        market_data = get_market_data(crop)

        # Get soil pH and moisture using the updated function (no await, synchronous)
        soil_data = ask_ollama_for_soil_data(location)

        # Get weather data based on location (no await, synchronous)
        weather = get_weather_data(location)

        # Get farming advice based on market, soil, and weather
        advice = get_farm_advice(market_data, soil_data["soil_ph"], weather)

        # Prepare the response data
        response_data = {
            "crop": crop,
            "soil PH": soil_data.get("soil_ph", "N/A"),  # Getting soil pH from the returned data
            "soil moisture": soil_data.get("soil_moisture", "N/A"),  # Getting soil moisture from the returned data
            "Temperature": weather,
            # "advice": advice  # Optional, include advice if you want
        }

        # Output the response to a JSON file
        with open("output.json", "w") as f:
            json.dump(response_data, f, indent=4)

        return response_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
