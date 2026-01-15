from app.extensions import db

class CommentLikeModel(db.Model):
    __tablename__ = "comment_likes"

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.String)
    comment_id = db.Column(db.String)
    user_uid = db.Column(db.String)
    comment_type = db.Column(db.String) # e.g., 'COMMENT', 'REPLY'
    created_date_timestamp = db.Column(db.Integer)
    updated_date_timestamp = db.Column(db.Integer)