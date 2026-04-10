import os
import time
import requests
from celery_worker import celery
from dotenv import load_dotenv

load_dotenv()

# print(os.environ.get("API_KEY"))






@celery.task(name="process_user_data")
def process_user_data(user_id, name):
    print(f"Starting work on: {user_id} == {name}")
    time.sleep(10) 
    print("Work finished!")
    return True





@celery.task(name="send_email") 
def send_email(user_id):
    URL = "https://servicestack.pythonanywhere.com/send-email"
    API_KEY = os.environ.get("EMAIL_API")
    RECIPIENT = "anything3628@gmail.com"

    payload = {
        "subject": "🚀 Deployment Test from CELERY using REDIS",
        "body": "<h1>Success!</h1><p>from CELERY using REDIS</p>",
        "receiver_email": RECIPIENT,
        "authority_name": f"Deepti celery=={user_id}",
        "body_type": "html"
    }

    headers = {
        "X-API-KEY": API_KEY,
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(URL, json=payload, headers=headers)
        result = f"Status {response.status_code}: {response.text}"
        print(result) # This will show up in your Railway Dashboard logs!
        
        if response.status_code == 202:
            return "✅ SUCCESS"
        else:
            return f"❌ FAILED: {result}"
        
    except Exception as e:
        return str(e)