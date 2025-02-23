# Weekly Side Hustle Generator
 This is a Telex integration that generates weekly side hustle for users.

   ![image alt](https://github.com/telexintegrations/Weekly-Side-Hustle-Generator/blob/6162adab4d95a6d0cc096677d27e4fa84348ab94/e34feed0-f174-4a58-a398-8e9c0a3c0693.JPG)

## Key Features
- Fetches trending side hustles every week
- Uses external APIs like Upwork and LinkedIn
- Provides curated gig economy opportunities
- Updated dynamically

## Tech Stack
- FastAPI
- HTTPX
- Telex Webhooks
- RapidAPI

## How to Setup the Integration in Telex
1. Login or create an account on Telex.
2. In your dashboard, navigate to the **Apps** section.
3. Click on the "Add App" button and enter this URL in the popup's input field:  
   `https://weekly-side-hustle-generator.onrender.com/integration.json`
4. Activate the app.
5. Authorize the app to link it to your Telex account.
6. After authorization, copy the token and add it to your settings in the **API Token** field.
7. Specify the interval using **cron syntax** to determine when the integration should run (e.g., "15 9,16 * * *" to run at 9:15 AM and 4:15 PM). You can use [crontab.guru](https://crontab.guru) to generate an interval.
8. Choose a channel to run the integration in the **Output tab**.

## How to Setup and Run the App Locally

### Clone the repository
```bash
git clone https://github.com/UgoBest100/weekly-side-hustle-generator.git
cd weekly-side-hustle-generator
```

### Install dependencies
```bash
pip install -r requirements.txt
```

### Run the application
```bash
uvicorn main:app --reload
```

### Run tests
```bash
pytest
```

### Use Postman to test the endpoints

## API Documentation

### `GET /integration.json`
Fetches the integration details for Telex.

### `POST /tick`
Fetches the specified side hustle jobs and sends a message to the specified channel on Telex.

#### Request Body:
```json
{
    "channel_id": "your-channel-id",
    "return_url": "your-return-url",
    "settings": [
        {
            "label": "API Token",
            "type": "text",
            "required": true,
            "default": "YOUR_TRELO_TOKEN"
        },
        {
            "label": "Interval",
            "type": "text",
            "required": true,
            "default": "* * * * *"
        }
    ]
}
```

#### Response (202 - Accepted):
```json
{
    "status": 202,
    "description": "Data received successfully!"
}
```

#### Response (500 - Internal Server Error):
```json
{
    "status": 500,
    "description": "Failed to run service!"
}
```

#### Response (500 - Internal Server Error):
```json
{
    "status": 429,
    "description": "You may have exceeded your API request limit."
}
```

---

### Author
Developed by UgoBest.

