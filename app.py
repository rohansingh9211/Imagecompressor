from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from celery import Celery
import pandas as pd
import os
import uuid
import requests
from PIL import Image
from io import BytesIO

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Rohan%40123@localhost/flask_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

PROCESSED_IMG_DIR = "processed_images"
os.makedirs(PROCESSED_IMG_DIR, exist_ok=True)

# WEBHOOK_URL = "http://your-webhook-url.com/notify"

@app.route('/')
def apps():
    return "app says hi"

import controllers.image_compressor as image_compressor
