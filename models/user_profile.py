from app.shared import db

class UserProfile(db.Model):
    __tablename__ = "user_profiles"

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String)
    email = db.Column(db.String(256))
    full_name = db.Column(db.String)
    photo = db.Column(db.String)