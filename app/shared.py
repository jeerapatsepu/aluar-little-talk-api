from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from uuid import uuid4
from google.cloud import bigquery

db = SQLAlchemy()
bcrypt = Bcrypt()
uid = uuid4()
bigqueryClient = bigquery.Client()