from app.shared import db

class PostRepostModel(db.Model):
    __tablename__ = "post_reposts"

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.String)
    user_uid = db.Column(db.String)
    created_date_timestamp = db.Column(db.Integer)
    updated_date_timestamp = db.Column(db.Integer)