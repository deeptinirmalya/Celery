import os
import threading
from celery import Celery
from flask import Flask
from dotenv import load_dotenv

load_dotenv()

# 1. Setup a tiny Flask app
app = Flask(__name__)



@app.route('/')
def health_check():
    return "Worker Heartbeat: OK", 200

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

celery = Celery(
    "worker",
    broker=os.getenv("CELERY_REDIS_URL"),
    include=["tasks"]
)


threading.Thread(target=run_flask, daemon=True).start()