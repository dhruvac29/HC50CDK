import json
import boto3
import os
import uuid

# Initialize the S3 client
s3_client = boto3.client("s3")

# Retrieve the bucket name from environment variables
bucket_name = os.environ["BUCKET_NAME"]


def handler(event, context):
    """
    Lambda function handler to generate a presigned URL for uploading a CSV file to S3.

    :param event: The event dictionary containing the request data.
    :param context: The context in which the function is called.
    :return: A response dictionary containing the presigned URL and unique key.
    """
    # Generate a unique key for the file
    unique_key = f"{uuid.uuid4()}.csv"

    # Generate a presigned URL for uploading the file
    presigned_url = s3_client.generate_presigned_url(
        "put_object",
        Params={"Bucket": bucket_name, "Key": unique_key, "ContentType": "text/csv"},
        ExpiresIn=300,  # URL expiration time in seconds (5 minutes)
        HttpMethod="PUT",
    )

    # Return the presigned URL and the unique key
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"url": presigned_url, "key": unique_key}),
    }
