import logging
import boto3
import datetime
import time
import os
from botocore.exceptions import ClientError
logger = logging.getLogger()

if len(logging.getLogger().handlers) > 0:
    logger = logging.getLogger()
    logging.getLogger().setLevel(logging.INFO)
else:
    logging.basicConfig(level=logging.INFO)

def logError (methodName, E, parameters):
    ErrorMessage = "fileMaker {} ERROR in {}: {}. Info: {}".format(os.getenv('functionName'),
                          methodName, E, parameters)
    logger.error(ErrorMessage)

def logInfo (methodName, parameters):
    InfoMessage = "fileMaker {} INFO in {}: Info: {}".format(os.getenv('functionName'),
                          methodName, parameters)
    logger.info(InfoMessage)

def send_file(fileName, object_name=None):
    bucket = "{}-{}".format(os.getenv("BUCKET_NAME"), os.getenv("ENVIRONMENT"))

    if object_name is None:
        object_name = fileName
    s3_client = boto3.client('s3',
        aws_access_key_id=os.getenv("ACCESS_KEY"),
        aws_secret_access_key=os.getenv("SECRET_ACCESS_KEY"))

    try:
        logInfo("send_file","Uploading: {} to {}. Objname: {}".format(fileName, bucket, object_name))
        response = s3_client.upload_file(fileName, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def create_file(dateStr):
    try:
        print(dateStr)
        f = open(dateStr,"w+")
        f.write("Programming is fun.")
        logInfo("create_file","File created. Ready to send")
        send_file(dateStr)
        f.close()
    except Exception as E:
        logError("create_file", E, {})
        pass

def main():
    while True:
        timestamp = datetime.datetime.now()
        dateStr = "{}{}{}-{}:{}:{}".format(
            '{:04}'.format(timestamp.year),
            '{:02}'.format(timestamp.month),
            '{:02}'.format(timestamp.day),
            '{:02}'.format(timestamp.hour),
            '{:02}'.format(timestamp.minute),
            '{:02}'.format(timestamp.second))
        logInfo("main",dateStr)
        create_file(dateStr)
        time.sleep(10)

if __name__ == "__main__":
    main()
