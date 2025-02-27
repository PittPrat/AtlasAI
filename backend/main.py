# Backend: FastAPI for AI-Powered Itinerary Platform

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List
import openai
import requests
import os
from dotenv import load_dotenv
import uvicorn

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# External API Keys
SKYSCANNER_API_KEY = os.getenv("SKYSCANNER_API_KEY")
GOOGLE_PLACES_API_KEY = os.getenv("GOOGLE_PLACES_API_KEY")

# Pydantic model for user input
class ItineraryRequest(BaseModel):
    destination: str
    budget: float
    interests: List[str]

# AI-generated itinerary
@app.post("/generate-itinerary")
def generate_itinerary(request: ItineraryRequest):
    try:
        prompt = f"Generate a travel itinerary for {request.destination} with a budget of ${request.budget}. Interests include: {', '.join(request.interests)}."
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "You are a travel planner AI."},
                      {"role": "user", "content": prompt}]
        )
        itinerary = response["choices"][0]["message"]["content"]
        return {"itinerary": itinerary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# API to fetch flight details (Skyscanner)
@app.get("/flights")
def get_flights(origin: str, destination: str, date: str):
    url = f"https://partners.api.skyscanner.net/apiservices/browseroutes/v1.0/US/USD/en-US/{origin}/{destination}/{date}?apiKey={SKYSCANNER_API_KEY}"
    response = requests.get(url)
    return response.json()

# API to fetch hotel details (Google Places)
@app.get("/hotels")
def get_hotels(destination: str):
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query=hotels+in+{destination}&key={GOOGLE_PLACES_API_KEY}"
    response = requests.get(url)
    return response.json()

# API to fetch restaurants (Google Places)
@app.get("/restaurants")
def get_restaurants(destination: str):
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query=restaurants+in+{destination}&key={GOOGLE_PLACES_API_KEY}"
    response = requests.get(url)
    return response.json()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
