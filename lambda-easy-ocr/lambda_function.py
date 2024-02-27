import io
import boto3
import os
import json
import easyocr
import numpy as np
import traceback
from PIL import Image

bucketName = os.environ.get('bucketName') # bucket name
s3_prefix = os.environ.get('s3_prefix')       
s3_client = boto3.client('s3') 
ocrLogTableName = os.environ.get('ocrLogTableName')      

def lambda_handler(event, context):
    print('event: ', event)
    
    requestId = event.get('requestId')    
    requestTime = event.get('requestTime') 
    key = s3_prefix + '/' + event.get('filename')
    target_languages = [
        "en",
        "ko"
    ]

    image_obj = s3_client.get_object(Bucket=bucketName, Key=key)
    image_content = image_obj['Body'].read()
    image = Image.open(io.BytesIO(image_content))
    image_np = np.array(image)

    reader = easyocr.Reader(
        target_languages,
        model_storage_directory='/tmp',
        user_network_directory='/tmp',
        download_enabled=True,
        gpu=False
    )
    results = reader.readtext(image_np)
    results = reader.readtext(image_np)

    detected_texts = []
    positions = []
    for result in results:
        text = result[1]
        detected_texts.append(text)

        position = result[0]
        top_left = [int(coord) for coord in position[0]]
        top_right = [int(coord) for coord in position[1]]
        bottom_right = [int(coord) for coord in position[2]]
        bottom_left = [int(coord) for coord in position[3]]
        positions.append({
            "Text": text,
            "TopLeft": {
                "x": top_left[0],
                "y": top_left[1]
            },
            "TopRight": {
                "x": top_right[0],
                "y": top_right[1]
            },
            "BottomRight": {
                "x": bottom_right[0],
                "y": bottom_right[1]
            },
            "BottomLeft": {
                "x": bottom_left[0],
                "y": bottom_left[1]
            }
        })

    detected_texts_join = ' '.join([result[1] for result in results])
    print('detected_texts_join: ', detected_texts_join)
    
    item = {    # save result
        'request_id': {'S':requestId},
        'request_time': {'S':requestTime},
        'key': {'S':detected_texts_join},
        'text': {'S':json.dumps(detected_texts)},
        'positions': {'S':json.dumps(positions)}
    }
    client = boto3.client('dynamodb')
    try:
        resp =  client.put_item(TableName=ocrLogTableName, Item=item)
        print('resp, ', resp)
    except Exception:
        err_msg = traceback.format_exc()
        print('error message: ', err_msg)
        raise Exception ("Not able to write into dynamodb")        
    
    return {
        'DetectedText': detected_texts_join,
        'DetectedResults': positions
    }