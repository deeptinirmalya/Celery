import os
import threading
from celery import Celery
from flask import Flask
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/')
def health_check():
    return "Worker Heartbeat: OK", 200

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)





celery = Celery(
    "mail_service",
    broker=os.getenv("CLOUDAMQP_URL"),
    include=['tasks']
)

celery.conf.update(
    # --- SPEED & SCALING ---
    broker_pool_limit=None,          
    task_acks_late=False,             
    worker_prefetch_multiplier=10,    
    
    # --- EVENT SILENCING (Saves Requests) ---
    worker_send_task_events=False,    
    task_send_sent_event=False,       
    
    # --- RELIABILITY ---
    broker_connection_retry_on_startup=True,
    broker_heartbeat=30,              
    
    # --- OPTIMIZATION ---
    task_compression='gzip',          
    task_ignore_result=True,          
)



# --------------------------------


# command for run on render =  python -m celery -A celery_worker:celery worker --loglevel=info --concurrency=4 --without-gossip --without-mingle --heartbeat-interval 30


threading.Thread(target=run_flask, daemon=True).start()