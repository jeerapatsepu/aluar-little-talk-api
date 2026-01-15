from app.extensions import db

class PostBookmarkModel(db.Model):
    __tablename__ = "post_bookmarks"

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.String)
    user_uid = db.Column(db.String)
    created_date_timestamp = db.Column(db.Integer)
    updated_date_timestamp = db.Column(db.Integer)