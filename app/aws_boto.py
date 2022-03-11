from datetime import datetime
from functools import lru_cache
import boto3
from botocore.exceptions import ClientError

from .models import Settings

@lru_cache()
def get_settings():
    return Settings()


bucket_name = "secai-text-summ-final-csv"
object_name = f"{datetime.today().strftime('%Y-%m-%d')}.csv"
# object_name = "2022-03-10.csv"


def create_presigned_url(
    bucket_name=bucket_name, object_name=object_name, expiration=3600
):

    # Generate a presigned URL for the S3 object
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=get_settings().aws_access_key_id,
        aws_secret_access_key=get_settings().aws_secret_key,
        config= boto3.session.Config(region_name='us-east-2', signature_version='s3v4')
    )
    try:
        response = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket_name, "Key": object_name},
            ExpiresIn=expiration,
            HttpMethod="GET"
        )
    except ClientError as e:
        print("error", e)
        return None

    # The response contains the presigned URL
    return response
