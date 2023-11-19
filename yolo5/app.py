import time
from pathlib import Path
from flask import Flask, request
from detect import run
import uuid
import yaml
from loguru import logger
import os
import boto3
import pymongo


images_bucket = os.environ['BUCKET_NAME']
MONGO_USER = os.environ['MONGO_USER']
MONGO_PASS = os.environ['MONGO_PASS']

with open("data/coco128.yaml", "r") as stream:
    names = yaml.safe_load(stream)['names']

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    # Generates a UUID for this current prediction HTTP request. This id can be used as a reference in logs to identify and track individual prediction requests.
    prediction_id = str(uuid.uuid4())

    logger.info(f'prediction: {prediction_id}. start processing')

    # Receives a URL parameter representing the image to download from S3
    img_name = request.args.get('imgName')

    original_img_path = os.path.abspath(f'/usr/src/app/{img_name}')

    s3_client = boto3.client('s3')

    s3_client.download_file(images_bucket, img_name, original_img_path)
    s3_client.delete_object(Bucket=images_bucket, Key=img_name)

    # TODO download img_name from S3, store the local image path in original_img_path
    #  The bucket name should be provided as an env var BUCKET_NAME.

    logger.info(f'prediction: {prediction_id}/{original_img_path}. Download img completed')

    # Predicts the objects in the image
    run(
        weights='yolov5s.pt',
        data='data/coco128.yaml',
        source=original_img_path,
        project='static/data',
        name=prediction_id,
        save_txt=True
    )

    logger.info(f'prediction: {prediction_id}/{original_img_path}. done')

    # This is the path for the predicted image with labels
    # The predicted image typically includes bounding boxes drawn around the detected objects, along with class labels and possibly confidence scores.
    predicted_img_path = f'static/data/{prediction_id}/{img_name}'
    predicted_img = "yolo5-input/"+img_name+"_pred.jpeg"
    s3_client.upload_file(predicted_img_path, images_bucket, predicted_img)

    # TODO Uploads the predicted image (predicted_img_path) to S3 (be careful not to override the original image).

    # Parse prediction labels and create a summary
    pred_summary_path = f'static/data/{prediction_id}/labels/{img_name.split(".")[0]}.txt'
    if pred_summary_path:
        with open(pred_summary_path) as f:
            labels = f.read().splitlines()
            labels = [line.split(' ') for line in labels]
            labels = [{
                'class': names[int(l[0])],
                'cx': float(l[1]),
                'cy': float(l[2]),
                'width': float(l[3]),
                'height': float(l[4]),
            } for l in labels]

        logger.info(f'prediction: {prediction_id}/{original_img_path}. prediction summary:\n\n{labels}')

        prediction_summary = {
            'prediction_id': prediction_id,
            'original_img_path': original_img_path,
            'predicted_img_path': predicted_img_path,
            'labels': labels,
            'time': time.time()
        }

        mongo_server = pymongo.MongoClient(f'mongodb+srv://{MONGO_USER}:{MONGO_PASS}@mongo.l74j5hs.mongodb.net/')
        mongo_database = mongo_server["yolo5-db"]
        mongo_collection = mongo_database["history"]
        mongo_collection.insert_one(prediction_summary)
        prediction_summary.pop('_id')
        # TODO store the prediction_summary in MongoDB

        return prediction_summary
    else:
        return f'prediction: {prediction_id}/{original_img_path}. prediction result not found', 404


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8081)
