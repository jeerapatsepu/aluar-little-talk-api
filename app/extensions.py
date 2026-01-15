from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from google.cloud import bigquery
import boto3, os
from botocore.client import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
# bigqueryClient = bigquery.Client()

boto_session = boto3.session.Session()
boto_client = boto_session.client(
    's3',
    region_name='sgp1',
    endpoint_url=os.getenv('S3_ENDPOINT'),
    aws_access_key_id=os.getenv('S3_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('S3_SECRET_KEY'),
    config=Config(s3={'addressing_style': 'virtual'})
)