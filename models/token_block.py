from app.shared import db

class TokenBlock(db.Model):
    __tablename__ = "token_blocks"

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String)
    created_date_timestamp = db.Column(db.Integer)