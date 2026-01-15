

from flask_jwt_extended import current_user
from app.models.post import Post
from app.models.user_relationship import UserRelationship
from app.extensions import db
from sqlalchemy import desc

from app.utils.short_post import ShortPost

def get_home_feed(request):
    filter = request["filter"]
    match filter:
        case "ALL":
            return __get_home_feed_filter_all(request)
        case "FOLLOW":
            return __get_home_feed_filter_follow(request)
        case _:
            return __get_home_feed_filter_all(request)

def __get_home_feed_filter_all(request):
    offset = request["offset"]
    limit = request["limit"]
    post_list = Post.query.order_by(desc(Post.created_date_timestamp)).filter(Post.visibility == "PUBLIC").offset(offset).limit(limit).all()
    return list(map(map_home_feed_to_short_post, post_list))

def __get_home_feed_filter_follow(request):
    offset = request["offset"]
    limit = request["limit"]
    try:
        post_list = (
            db.session.query(Post)
            .join(UserRelationship, UserRelationship.receiver_id == Post.owner_uid)
            .filter(UserRelationship.sender_id == current_user.uid)
            .filter(Post.visibility == "PUBLIC")
            .order_by(desc(Post.created_date_timestamp))
            .offset(offset)
            .limit(limit)
            .all()
        )
        return list(map(map_home_feed_to_short_post, post_list))
    except Exception:
        return []
    
def map_home_feed_to_short_post(post_model):
    return ShortPost(post_model.post_id).get_post()