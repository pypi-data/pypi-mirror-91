import os
import sys
import logging
from os import environ
import boto3
import threading
from botocore.exceptions import ClientError
from typing import Text, Optional
from storage_script.progress import ProgressPercentage


def download_file(model: Text, folder: Text):
    """Download a model to an S3 bucket

    :param model: model to download
    :param folder: S3 object name. 
    :return: True if file was downloaded, else False
    """
    s3_client = boto3.client("s3")
    try:
        response = s3_client.download_file(
            os.environ.get("AWS_S3_BUCKET_RASA_MODELS"),
            folder + "/" + model,
            model,
            Callback=ProgressPercentage(
                folder + "/" + model,
                s3_client,
                os.environ.get("AWS_S3_BUCKET_RASA_MODELS"),
            ),
        )
    except ClientError as e:
        logging.error(e)
        return False
    return True
