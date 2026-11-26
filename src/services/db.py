"""
This file contains the mysql database configuration
"""

from typing import Dict
import mysql.connector
from mysql.connector import Error
from src.config import logging
from functools import lru_cache
import src.config as config
import boto3
from botocore.exceptions import ClientError
from src.services.baseModel import Response


def rds_connection(
    host: str, database: str, username: str, password: str, port: int
) -> Dict:
    dict = {}
    retry = 0
    try:
        connection = mysql.connector.connect(
            host=host, database=database, user=username, password=password, port=port
        )
        if connection.is_connected():
            connection.autocommit = False  # type: ignore
            db_Info = connection.get_server_info()
            logging.info("Connected to MySQL Server version " + str(db_Info))
            cursor = connection.cursor()
            connection.autocommit = True  # type: ignore
            dict["cursor"] = cursor
            dict["connection"] = connection
            return dict
            # get all records
        else:
            if retry != 5:
                logging.warning("retry database connection :" + str(retry))
                retry += 1
                rds_connection(host, database, username, password, port)
            else:
                logging.error(
                    {
                        "message": f"Failed to connect to {database} check credentials !!",
                        "line": format(sys.exc_info()[-1].tb_lineno),  # type: ignore
                    }
                )

    except Error as e:
        logging.error(
            {
                "message": "Failed to connect to RDS database",
                "error": str(e),
                "line": e.__traceback__.tb_lineno if e.__traceback__ else None,
            }
        )
    finally:
        return dict


# @lru_cache
def get_connection_objects() -> Dict:
    return rds_connection(
        config.MYSQL_HOST,
        config.MYSQL_DATABASE,
        config.MYSQL_USER,
        config.MYSQL_PASSWORD,
        config.MYSQL_PORT,
    )


# Create AWS session with credentials. using boto3 lib
session = boto3.Session(
    aws_access_key_id=config.ACCESS_KEY,
    aws_secret_access_key=config.SECRETE_ACCESS_KEY,
    region_name=config.REGION,
)

# Get arguments that are passed when running the script
s3Resource = boto3.resource(
    "s3",
    aws_access_key_id=config.ACCESS_KEY,
    aws_secret_access_key=config.SECRETE_ACCESS_KEY,
)
s3Client = boto3.client(
    "s3",
    aws_access_key_id=config.ACCESS_KEY,
    aws_secret_access_key=config.SECRETE_ACCESS_KEY,
)


def bucketNameValidation(BucketName):
    val = 0
    print(s3Resource.buckets.all())
    try:
        for bucket in s3Resource.buckets.all():
            # s3BucketList.append(bucket.name)
            # print(bucket)
            if BucketName == bucket.name:
                message = 1
                break
            else:
                continue

    except Exception as e:
        logging.error(e)
        val = 3
    finally:
        return val


def createBucket(bucketName, region=None) -> list:
    """Create an S3 bucket in a specified region

    If a region is not specified, the bucket is created in the S3 default
    region (None).
    """
    BucketName = bucketName
    message = ""
    bool = False
    # Create bucket
    try:
        if bucketNameValidation(BucketName) == 0:
            if region is None:
                s3Client.create_bucket(Bucket=BucketName)
            else:
                location = {"LocationConstraint": region}
                s3Client.create_bucket(
                    Bucket=BucketName, CreateBucketConfiguration=location
                )
                message = f"Successfully created {BucketName} Bucket"
                bool = True
                # logging.info("Bucket created !!!")
        else:
            message = f"{BucketName} Already exixts! No action taken"
            bool = True
            logging.info("Bucket exists !!!")
    except ClientError as e:
        logging.error(format(sys.exc_info()[-1].tb_lineno))  # type: ignore
        logging.error(e)
        message = str(e)
        bool = False
    finally:
        return [message, bool]


def create_s3_configuration_buckets() -> Response:
    error = "No error"
    try:
        message1, bool1 = createBucket(config.STAGING_RAW_DATA_BUCKET, config.REGION)
        # createBucket(config.PROCESSED_DATA_BUCKET, config.REGION)
        if bool1 is False:
            raise Exception(message1)
        message2, bool2 = createBucket(config.PROCESSED_DATA_BUCKET, config.REGION)
        if bool2 is False:
            raise Exception(message2)
    except Exception as e:
        error = e
    finally:
        message = f"{config.STAGING_RAW_DATA_BUCKET} bucket : {message1} \n {config.PROCESSED_DATA_BUCKET} bucket: {message2}"
        return Response(message=message, error=str(error))


response = create_s3_configuration_buckets()
print(response.message)
