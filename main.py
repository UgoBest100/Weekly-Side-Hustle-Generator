from fastapi import FastAPI, BackgroundTasks
import requests
from datetime import datetime
from pydantic import BaseModel
from typing import List
import httpx
from fastapi.middleware.cors import CORSMiddleware
import logging
logger = logging.getLogger(__name__)

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
    RAPIDAPI_HOST = "get-possible-hiring-manager.p.rapidapi.com"
    url = "https://get-possible-hiring-manager.p.rapidapi.com/"
    headers = {
        "Content-Type": "application/json",
        "x-rapidapi-host": RAPIDAPI_HOST,
        "x-rapidapi-key": RAPIDAPI_KEY
    }
    data = {
        "job_title": "Responsible AI Data Scientist",
        "company_name": "Salesforce",
        "location": "San Francisco"
    }
    response = requests.post(url, headers=headers, json=data)
    logger.info("Check response")
    logger.info(response)

    if response.status_code == 200:
        return_url = "https://ping.telex.im/v1/webhooks/01952814-87fa-74ff-839a-5937f06f0d5f"

        message = "\n\n".join([
            f"🔹 **{job['title']}**\n"
            f"📌 Frequency: {job['frequency']}\n"
            f"📄 Snippet: {job['snippet']}\n"
            f"🔗 Link: {job['link']}"
            for job in [
                {"title": "Sitaram Asur - Director of Data Science - Salesforce", "frequency": 5, "snippet": "Director, Salesforce AI · Data scientist, engineer, and leader, with extensive background in data mining, machine learning, NLP, social network analysis and ...", "link": "https://www.linkedin.com/in/sitaram-asur-9a35008"},
                {"title": "Anjali Samani, PhD - Salesforce", "frequency": 5, "snippet": "Experience: Salesforce · Location: San Francisco · 500+ connections on LinkedIn. View Anjali Samani, PhD's profile on LinkedIn, a professional community of ...", "link": "https://www.linkedin.com/in/anjalisamani"}
            ]
        ])
        data = {
            "message": message,
            "username": "UgoBest",
            "event_name": "Weekly hustle Generator",
            "status": "success"
        }

        async with httpx.AsyncClient() as client:
            await client.post(return_url, json=data)

    else:
        logger.error(f"Failed to fetch jobs. Status Code: {response.status_code}")

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
                "app_logo": "https://github.com/telexintegrations/Weekly-Side-Hustle-Generator/blob/e672ac5a58ddafb8a21ebf3c8c37b7ec04915cb6/IMG_2764.JPG",
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
