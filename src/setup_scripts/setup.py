import boto3
from botocore.exceptions import ClientError
import logging
import sys

from dotenv import load_dotenv
import os

################################# Logging ###############################################
# All application logs are saved in producer.log file in project directory
logging.basicConfig(
    format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
    handlers=[
        logging.FileHandler("producer.log"),
        logging.StreamHandler(sys.stdout),
    ],
)

load_dotenv()


# AWS Credentials -->
ACCESS_KEY = os.getenv("ACCESS_KEY")
SECRETE_ACCESS_KEY = os.getenv("SECRET_ACCESS_KEY")
REGION = "eu-west-1"
BUCKET_NAME_STAGING_DATA = "ep011-808429836131-eu-north-1-staging-bucket"
BUCKET_NAME_PROCESSED_DATA = "ep011-808429836131-eu-north-1-processed-bucket"
BUCKET_NAME_STAGING_SCRIPTS = "ep011-808429836131-eu-north-1-staging-scripts"
