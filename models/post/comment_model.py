from app.shared import db

class CommentModel(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    comment_uid = db.Column(db.String)
    text = db.Column(db.String)
    image_url = db.Column(db.String)
    parent_comment_uid = db.Column(db.String)
    post_id = db.Column(db.String)
    user_uid = db.Column(db.String)
    created_date_timestamp = db.Column(db.Integer)
    updated_date_timestamp = db.Column(db.Integer)