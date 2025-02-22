# Weekly Side Hustle Generator

## Overview
The **Weekly Side Hustle Generator** is a FastAPI-based Telex integration that fetches and delivers weekly side hustle ideas. It utilizes an external API to curate relevant job opportunities and sends them to Telex channels at scheduled intervals.

## Features
- Fetches trending side hustle opportunities.
- Uses external APIs like Upwork and LinkedIn.
- Provides curated gig economy opportunities.
- Dynamically updates job listings.
- Sends results to Telex channels using the tick-based interval system.

## Installation and Setup
### Prerequisites
Ensure you have the following installed:
- Python 3.9+
- FastAPI
- Uvicorn
- Requests
- HTTPX
- Pydantic

### Installation
1. Clone this repository:
   ```sh
   git clone https://github.com/yourusername/weekly-side-hustle-generator.git
   cd weekly-side-hustle-generator
   ```

2. Install the required dependencies:
   ```sh
   pip install -r requirements.txt
   ```

### Running the Application
Start the FastAPI server using Uvicorn:
   ```sh
   uvicorn main:app --reload
   ```
The application will be available at `http://127.0.0.1:8000`.

## API Endpoints

### 1. Fetch Weekly Side Hustles
   - **Endpoint:** `GET /weekly-hustles/`
   - **Description:** Fetches and returns weekly side hustles dynamically when requested.
   - **Response:**
     ```json
     {
       "weekly_hustles": [
         {
           "title": "Freelance Graphic Designer",
           "snippet": "Design engaging graphics for clients...",
           "link": "https://upwork.com/job-id"
         }
       ]
     }
     ```

### 2. Telex Integration Specification
   - **Endpoint:** `GET /integration.json`
   - **Description:** Returns the integration JSON required for Telex.
   - **Response:**
     ```json
     {
       "data": {
         "app_name": "Weekly Side Hustle Generator",
         "app_description": "Provides weekly side hustle ideas.",
         "app_logo": "https://postimg.cc/bGS5k8hm",
         "app_url": "https://weekly-side-hustle-generator.onrender.com",
         "integration_category": "Finance & Payments",
         "integration_type": "interval",
         "tick_url": "https://weekly-side-hustle-generator.onrender.com/tick/",
         "is_active": true
       }
     }
     ```

### 3. Telex Tick Endpoint
   - **Endpoint:** `POST /tick`
   - **Description:** Triggers the retrieval and dispatch of side hustle recommendations to the Telex channel.
   - **Payload:**
     ```json
     {
       "channel_id": "12345",
       "return_url": "https://ping.telex.im/v1/webhooks/...",
       "settings": [
         { "label": "interval", "type": "text", "required": true, "default": "* * * * *" }
       ]
     }
     ```
   - **Response:**
     ```json
     { "status": "accepted" }
     ```

## Deployment
This application can be deployed using **Render**, **Heroku**, or **Docker**.

### Deploying on Render
1. Push your repository to GitHub.
2. Create a new **Render Web Service**.
3. Connect it to your GitHub repository.
4. Set the Start Command as:
   ```sh
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```
5. Deploy and access your app at `https://your-deployed-api.onrender.com`

### Deploying with Docker
1. Create a `Dockerfile`:
   ```dockerfile
   FROM python:3.9
   WORKDIR /app
   COPY . /app
   RUN pip install --no-cache-dir -r requirements.txt
   CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
   ```
2. Build and run the container:
   ```sh
   docker build -t weekly-side-hustle .
   docker run -p 8000:8000 weekly-side-hustle
   ```

## Author
Developed by **UgoBest** for the HNG Internship Telex Integration Stage 3 Task.

## License
This project is open-source and available under the **MIT License**.

