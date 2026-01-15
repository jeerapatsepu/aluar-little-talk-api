from app.extensions import db

class USLI(db.Model):
    __tablename__ = "uslis"

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String)
    email = db.Column(db.String(256))
    full_name = db.Column(db.String)
    user_identifier = db.Column(db.String)