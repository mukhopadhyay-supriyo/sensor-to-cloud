"""Project-level configuration placeholder.

Keep non-secret defaults here. Load credentials and deployment-specific values
from environment variables .
"""

import boto3
from botocore.exceptions import ClientError
import logging
import sys
import random
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
SECRETE_ACCESS_KEY = os.getenv("SECRETE_ACCESS_KEY")
REGION = os.getenv("REGION")


# --- MySQL (used when DATA_SOURCE=mysql) -------------------------------------------------------
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", "3306"))
MYSQL_USER = os.getenv("MYSQL_USER", "")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "")


# ---- S3 Bucket names ----------------------------->
STAGING_RAW_DATA_BUCKET = os.getenv("STAGING_RAW_DATA_BUCKET", "")
PROCESSED_DATA_BUCKET = os.getenv("PROCESSED_DATA_BUCKET", "")


# ----- MQTT Configurations -------------------------->
BROKER = os.getenv("BROKER", "")
PORT = os.getenv("PORT", "")
TOPIC = os.getenv("TOPIC", "")
CLIENT_ID = f"python-mqtt-{random.randint(0, 1000)}"
