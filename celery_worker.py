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

    worker_send_task_events=False,    
    task_send_sent_event=False,       
    broker_pool_limit=1,              
    
    task_acks_late=True,              
    worker_prefetch_multiplier=1,     
    broker_connection_retry_on_startup=True,
    

    task_compression='gzip',          
    task_ignore_result=True,          
)



# --------------------------------


# for now == python -m celery -A celery_worker:celery worker --loglevel=info --concurrency=1 --without-gossip --without-mingle --heartbeat-interval 120
# for leter == python -m celery -A celery_worker:celery worker --loglevel=info --concurrency=1 --without-gossip --without-mingle

threading.Thread(target=run_flask, daemon=True).start()