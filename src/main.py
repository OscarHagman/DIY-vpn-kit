import json
import boto3
from botocore.config import Config

my_config = Config(
    region_name='eu-north-1',
    signature_version='v4',
    retries={
        'max_attempts': 10,
        'mode': 'standard'
    }
)

with open("secrets.json", "r") as json_keys:
    keys = json.load(json_keys)

ec2 = boto3.client(
    'ec2',
    config=my_config,
    aws_access_key_id=keys["aws_access_key_id"],
    aws_secret_access_key=keys["aws_secret_access_key"]
)
response = ec2.describe_instances()
print(response)
