

import os
import uuid
import pandas as pd
import requests
from io import BytesIO
from PIL import Image
# from config import PROCESSED_IMG_DIR, PROCESSED_CSV_DIR, WEBHOOK_URL
from celery import Celery

celery = Celery(__name__)

@celery.task(bind=True)
def process_images(self, request_id, csv_filename):
    try:
        # Ensure directories exist
        os.makedirs(PROCESSED_IMG_DIR, exist_ok=True)
        os.makedirs(PROCESSED_CSV_DIR, exist_ok=True)

        # Load CSV file
        df = pd.read_csv(csv_filename)
        output_urls = []

        for index, row in df.iterrows():
            input_urls = row["Input Image Urls"].split(",")
            processed_images = []

            for img_url in input_urls:
                img_url = img_url.strip()
                response = requests.get(img_url)

                if response.status_code == 200:
                    img = Image.open(BytesIO(response.content))
                    
                    # Compress image (50% quality)
                    output_filename = f"{uuid.uuid4()}.jpg"
                    output_path = os.path.join(PROCESSED_IMG_DIR, output_filename)
                    img.save(output_path, "JPEG", quality=50)

                    # Store processed image path
                    processed_images.append(output_path)

            # Append processed image URLs
            output_urls.append(",".join(processed_images))

        # Add output image URLs to CSV
        df["Output Image Urls"] = output_urls
        output_csv_filename = os.path.join(PROCESSED_CSV_DIR, f"processed_{request_id}.csv")
        df.to_csv(output_csv_filename, index=False)

        # Update database
        # task = ImageProcessingTask.query.get(request_id)
        # if task:
        #     task.status = "completed"
        #     task.output_csv = output_csv_filename
        #     db.session.commit()
        model.update_csv_storage_system(id=request_id, output_csv=output_csv_filename, status="Complete")

        # Trigger webhook
        # try:
        #     requests.post(WEBHOOK_URL, json={"request_id": request_id, "status": "completed", "output_csv": output_csv_filename})
        # except requests.RequestException as e:
        #     print(f"Webhook error: {e}")

    except Exception as e:
        model.update_csv_storage_system(id=request_id, status="Failed")
        print(f"Error processing images: {e}")
