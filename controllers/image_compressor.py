from flask import Flask, request, jsonify
from celery import Celery
import pandas as pd
import os
import uuid
import requests
from PIL import Image
from io import BytesIO
from flask import Blueprint
from app import app
from async_folder.image_compress_util import process_images
from model.model import Models

model = Models()

@app.route('/upload', methods=['POST'])
def upload_csv():
    model.csv_storage_system()
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    
    if not file.filename.endswith('.csv'):
        return jsonify({"error": "Only CSV files are allowed"}), 400

    df = pd.read_csv(file)
    
    required_columns = ["Serial Number", "Product Name", "Input Image Urls"]
    if not all(col in df.columns for col in required_columns):
        return jsonify({"error": "Invalid CSV format"}), 400
    
    request_id = str(uuid.uuid4())
    csv_filename = f"{request_id}.csv"
    file.save(csv_filename)

    model.create_csv_storage_system(id=request_id, input_csv=csv_filename, status="pending")
    process_images.delay(request_id, csv_filename)

    return jsonify({"request_id": request_id, "status": "Processing Started"}), 200
