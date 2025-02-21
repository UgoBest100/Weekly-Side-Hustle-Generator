from fastapi import FastAPI, BackgroundTasks
import requests
from datetime import datetime
from pydantic import BaseModel
from typing import List
import httpx
import asyncio
from fastapi.middleware.cors import CORSMiddleware



class Setting(BaseModel):
    label: str
    type: str
    required: bool
    default: str

class Payload(BaseModel):
    channel_id: str
    return_url: str
    settings: List[Setting]

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def fetch_weekly_side_hustles(payload: Payload):
    """Fetch side hustle ideas from the API and return them."""
    RAPIDAPI_KEY = "a9d4db2b83msh316d2d491587ab9p1e01b8jsn5c2a93b4c275"
    RAPIDAPI_HOST = "jsearch.p.rapidapi.com"
    url = "https://jsearch.p.rapidapi.com/search"
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": RAPIDAPI_HOST
    }
    params = {"query": "side hustle", "num_pages": "1"}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        results = response.json().get("data", [])
        return_url = payload["return_url"]
        message = "\n".join([result for result in results if result is not None])
        data = {
            "message": message,
            "username": "UgoBest",
            "event_name": "Weekly hustle Generator",
            "status": "error"
        }

        async with httpx.AsyncClient() as client:
            await client.post(payload.return_url, json=data)


    else:
        return {"error": f"Failed to fetch jobs. Status Code: {response.status_code}"}


#####@app.get("/weekly-hustles/")
#def get_weekly_hustles():
    """Fetch and return weekly side hustles dynamically when requested."""
    #side_hustles = fetch_weekly_side_hustles()  # Call function inside endpoint
    #if not side_hustles:
        #return {"message": "No side hustles available yet. Please check later."}
   # return {"weekly_hustles": side_hustles}

@app.get("/integration.json")
def telex_integration():
    """Telex integration JSON endpoint."""
    return {
        "data": {
            "date": {
                "created_at": datetime.now().strftime("%Y-%m-%d"),
                "updated_at": datetime.now().strftime("%Y-%m-%d")
            },
            "descriptions": {

                "app_description": "Provides weekly side hustle ideas.",
                "app_logo": "https://postimg.cc/bGS5k8hm",
                "app_name": "Weekly Side Hustle Generator",
                "app_url": "https://weekly-side-hustle-generator.onrender.com",
                "background_color": "#FF5733"
            },
            "integration_category": "Finance & Payments",
            "integration_type": "interval",
            "is_active": True,
            "author": "UgoBest",
            "key_features": [
                "Fetches trending side hustles every week",
                "Uses external APIs like Upwork and LinkedIn",
                "Provides curated gig economy opportunities",
                "Updated dynamically"
            ],
            "settings": [
                {
                    "label": "interval",
                    "type": "text",
                    "required": True,
                    "default": "* * * * *"
                }
            ],
            "tick_url": "https://weekly-side-hustle-generator.onrender.com/tick/",
            "target_url": ""
        }
    }
@app.post("/tick", status_code=202)
def monitor(payload: Payload, background_tasks: BackgroundTasks):
    background_tasks.add_task(fetch_weekly_side_hustles, payload)
    return {"status": "accepted"}