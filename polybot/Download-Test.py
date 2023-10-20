import os
import boto3



try:
    object = input("""Hello!
    Please select from which objects you wish to download the wanted content:
    data/
    dist/
    images/
    internal/
    RDS-Export/
    yolo5-input/
    Make sure to type it as you see and include the name of the file: """)
    bucket_name = 'hbd-bucket1'
    file_name = input("What will be the file's name?: ")
    file_destination = os.path.abspath(f'/home/devops/docker/Docker_Bot/polybot/photos/{file_name}')
    s3_client = boto3.client('s3')
    s3_client.download_file(bucket_name, object, file_destination)
except FileNotFoundError as e:
    print(f'''The following error has occurred:
    {e}''')









