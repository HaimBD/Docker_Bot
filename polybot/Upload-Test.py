import os
import boto3



try:
    file_input = input("""
    Hello!
    Welcome to the HBD bucket service.
    Please input the absolute file path of the needed file to upload: """)
    file = os.path.abspath(file_input)
    bucket = 'hbd-bucket1'
    object = input("""
    These are the existing folders that you can upload to:
    data/
    dist/
    images/
    internal/
    RDS-Export/
    yolo5-input/
    Please make sure you type it correctly with the right casing and add the name of the file: """)

    s3_client = boto3.client('s3')
    s3_client.upload_file(file, bucket, object)
except FileNotFoundError as e:
    print(f'The following error has occurred: {e}')







