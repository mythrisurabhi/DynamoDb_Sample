import boto3


def create_dynamodb_resource():
    return boto3.resource("dynamodb", region_name="localhost", endpoint_url="http://localhost:8000/",
                          aws_access_key_id="gi8vsa", aws_secret_access_key="xl2cta")
