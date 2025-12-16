from app.shared import db

class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.String)
    owner_uid = db.Column(db.String)
    visibility = db.Column(db.String)
    type = db.Column(db.String)
    original_post_id = db.Column(db.String)
    like_count = db.Column(db.Integer)
    comment_count = db.Column(db.Integer)
    created_date_timestamp = db.Column(db.Integer)
    updated_date_timestamp = db.Column(db.Integer)

class PostContent(db.Model):
    __tablename__ = "post_contents"

    id = db.Column(db.Integer, primary_key=True)
    content_id = db.Column(db.String)
    index = db.Column(db.Integer)
    post_id = db.Column(db.String)
    type = db.Column(db.String)
    text = db.Column(db.String)
    text_type = db.Column(db.String)

class PostImageContent(db.Model):
    __tablename__ = "post_image_contents"

    id = db.Column(db.Integer, primary_key=True)
    index = db.Column(db.Integer)
    post_id = db.Column(db.String)
    content_id = db.Column(db.String)
    image_content_id = db.Column(db.String)
    link = db.Column(db.String)