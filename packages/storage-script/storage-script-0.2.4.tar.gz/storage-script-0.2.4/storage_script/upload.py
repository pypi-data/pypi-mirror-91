import os
import sys
import logging
from os import environ
import boto3
import threading
from botocore.exceptions import ClientError
from typing import Text, Optional
from storage_script.progress import ProgressPercentage


def upload_file(model: Text, folder: Text):
    """Upload a model to an S3 bucket

    :param model: model to upload
    :param folder: S3 object name. 
    :return: True if file was uploaded, else False
    """
    # Upload the file
    s3_client = boto3.client("s3")
    try:
        modelName = os.path.basename(model)
        response = s3_client.upload_file(
            model,
            os.environ.get("AWS_S3_BUCKET_RASA_MODELS"),
            folder + "/" + modelName,
            Callback=ProgressPercentage(model),
        )
    except ClientError as e:
        logging.error(e)
        return False
    return True
