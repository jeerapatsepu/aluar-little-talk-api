from app.shared import db

class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.String)
    title = db.Column(db.String(256))
    description = db.Column(db.String(1000))
    owner_uid = db.Column(db.String)
    photo = db.Column(db.String)
    visibility = db.Column(db.String)
    type = db.Column(db.String)
    original_post_id = db.Column(db.String)
    like_count = db.Column(db.Integer)
    comment_count = db.Column(db.Integer)
    created_date_timestamp = db.Column(db.Integer)
    updated_date_timestamp = db.Column(db.Integer)
    