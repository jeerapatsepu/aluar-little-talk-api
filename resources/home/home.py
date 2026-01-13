# import logging
import uuid
from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import current_user, jwt_required
from datetime import datetime, timezone
from models.post.post import Post
from models.profile.user_relationship import UserRelationship
from resources.short_post import ShortPost
from resources.profile.post.profile_posts_response import ProfilePostsResponseSchema
from schemas.reponse_schema.meta import MetaSchema
from schemas.request_schema.home_feed_request_schema import HomeFeedRequestSchema
from app.shared import db

blp = Blueprint("Home", __name__, description="Home")

@blp.route("/home/feed")
class Home(MethodView):
    @jwt_required(optional=True)
    @blp.arguments(HomeFeedRequestSchema)
    @blp.response(200, ProfilePostsResponseSchema)
    def post(self, request):
        offset = request["offset"]
        limit = request["limit"]
        filter = request["filter"]
        posts = []
        match filter:
            case "ALL":
                posts = Post.query.order_by(Post.created_date_timestamp).filter(Post.visibility == "PUBLIC").offset(offset).limit(limit).all()
            case "FOLLOW":
                try:
                    posts = (
                        db.session.query(Post)
                        .join(UserRelationship, UserRelationship.receiver_id == Post.owner_uid)
                        .filter(UserRelationship.sender_id == current_user.uid)
                        .filter(Post.visibility == "PUBLIC")
                        .order_by(Post.created_date_timestamp)
                        .offset(offset)
                        .limit(limit)
                        .all()
                    )
                except Exception:
                    posts = []
            case "FRIENDS":
                try:
                    posts = (
                        db.session.query(Post)
                        .join(UserRelationship, UserRelationship.receiver_id == Post.owner_uid and UserRelationship.sender_id == Post.owner_uid)
                        .filter(Post.visibility == "FRIENDS")
                        .filter(Post.owner_uid != current_user.uid)
                        .filter(UserRelationship.receiver_id == current_user.uid and UserRelationship.sender_id == Post.owner_uid or UserRelationship.sender_id == current_user.uid and UserRelationship.receiver_id == Post.owner_uid)
                        .order_by(Post.created_date_timestamp)
                        .offset(offset)
                        .limit(limit)
                        .all()
                    )
                except Exception:
                    posts = []
            case _:
                posts = Post.query.order_by(Post.created_date_timestamp).filter(Post.visibility == "PUBLIC").offset(offset).limit(limit).all()
        posts.sort(key=self.__sortPostsList, reverse=True)
        new_posts = self.__getShortPost(posts=posts)
        return self.__getPofilePostsSuccessResponse(new_posts)

    def __getShortPost(self, posts: list):
        short_post_list = []
        for post in posts:
            short_post = ShortPost(post_id=post.post_id).get_post()
            short_post_list.append(short_post)
        return short_post_list

    def __sortPostsList(self, e):
        return e.created_date_timestamp

    def __getPofilePostsSuccessResponse(self, posts):
        time = datetime.now(timezone.utc)

        meta = MetaSchema()
        meta.response_id = uuid.uuid4().hex
        meta.response_code = 1000
        meta.response_date = str(time)
        meta.response_timestamp = str(time.timestamp())
        meta.error = None

        response = ProfilePostsResponseSchema()
        response.meta = meta
        response.data = posts
        return response