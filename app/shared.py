from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from uuid import uuid4

db = SQLAlchemy()
bcrypt = Bcrypt()
uid = uuid4()