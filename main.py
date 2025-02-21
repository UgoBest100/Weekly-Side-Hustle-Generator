from fastapi import FastAPI, BackgroundTasks
import requests
from datetime import datetime
from pydantic import BaseModel
from typing import List
import httpx
import asyncio
from fastapi.middleware.cors import CORSMiddleware
import logging



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

import asyncio

async def fetch_weekly_side_hustles(payload):
    """Fetch side hustle ideas from the API and return them."""
    RAPIDAPI_KEY = "a9d4db2b83msh316d2d491587ab9p1e01b8jsn5c2a93b4c275"
    RAPIDAPI_HOST = "jsearch.p.rapidapi.com"
    url = "https://jsearch.p.rapidapi.com/search"
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": RAPIDAPI_HOST
    }
    params = {"query": "side hustle", "num_pages": "1"}
    logger = logging.getLogger(__name__)
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers, params=params)
            response.raise_for_status()  # Raise an exception for 4xx/5xx responses
            data = response.json()
        logger.info(data)
        results = data.get("weekly_hustles", [])
        if not results:
            return {"error": "No side hustles found."}
        return_url = "https://ping.telex.im/v1/webhooks/01952814-87fa-74ff-839a-5937f06f0d5f"
        message = "\n\n".join([
            f":small_blue_diamond: *{job['job_title']}*\n"
            f":drawing_pin: Employer: {job['employer_name']}\n"
            f":globe_with_meridians: Website: {job.get('employer_website', 'N/A')}\n"
            f":round_drawing_pin: Location: {job.get('job_location', 'Remote' if job['job_is_remote'] else 'N/A')}\n"
            f":clock3: Employment Type: {job.get('job_employment_type', 'N/A')}\n"
            f":briefcase: Published By: {job.get('job_publisher', 'N/A')}\n"
            f":date: Posted: {job.get('job_posted_at', 'N/A')}\n"
            f":page_facing_up: Description: {job.get('job_description', 'N/A')[:300]}...\n"
            f":zap: Benefits: {', '.join(job.get('job_highlights', {}).get('Benefits', ['N/A']))}\n"
            f":dart: Qualifications: {', '.join(job.get('job_highlights', {}).get('Qualifications', ['N/A']))}\n"
            f":link: Apply Here: {job['job_apply_link']}"
            for job in results
        ])
        payload_data = {
            "message": message,
            "username": "UgoBest",
            "event_name": "Weekly Hustle Generator",
            "status": "success"
        }
        async with httpx.AsyncClient() as client:
            await client.post(return_url, json=payload_data)
        return payload_data
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error occurred: {e}")
        return {"error": f"Failed to fetch jobs. Status Code: {e.response.status_code}"}
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return {"error": f"An unexpected error occurred: {str(e)}"}

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