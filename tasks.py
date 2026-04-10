import os
import requests
from celery_worker import celery
from dotenv import load_dotenv


load_dotenv()


@celery.task(
    name="process_user_data",
    bind=True, 
    max_retries=3, 
    default_retry_delay=60 
)
def process_user_data(self, user_id, name):
    print(f"Starting work on: {user_id} == {name}")
    print(f"work done on: {user_id} == {name}")
    return True




@celery.task(
    name="process_email_task",
    bind=True, 
    max_retries=3, 
    default_retry_delay=60  
)
def process_email_task(self, email):
    URL = "https://servicestack.pythonanywhere.com/send-email"
    API_KEY = os.environ.get("EMAIL_API")
    RECIPIENT = str(email)
    

    payload = {
        "subject": "🚀 Deployment Test from CELERY using REDIS",
        "body": "<h1>Success!</h1><p>from CELERY using REDIS</p>",
        "receiver_email": RECIPIENT,
        "authority_name": f"from local",
        "body_type": "html"
    }

    headers = {
        "X-API-KEY": API_KEY,
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(URL, json=payload, headers=headers)
        result = f"Status {response.status_code}: {response.text}: email ={email}"
        print("email:", RECIPIENT)
        
        if response.status_code == 202:
            return f"✅ SUCCESS == {result}"
        else:
            # This makes sure the task is RETRIED instead of lost
            print(f"Email to {RECIPIENT}: ❌ API Error {response.status_code}")
            raise self.retry(countdown=60)

        
    except Exception as e:
        raise self.retry(exc=e)