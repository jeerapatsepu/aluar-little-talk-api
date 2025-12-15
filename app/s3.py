import boto3, os
from botocore.client import Config

session = boto3.session.Session()
client = session.client(
    's3',
    region_name='sgp1',
    endpoint_url=os.getenv('S3_ENDPOINT'),
    aws_access_key_id=os.getenv('S3_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('S3_SECRET_KEY'),
    config=Config(s3={'addressing_style': 'virtual'})
)

# client.create_bucket(Bucket='my-new-space')
# print([b['Name'] for b in client.list_buckets()['Buckets']])

