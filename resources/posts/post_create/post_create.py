from flask import jsonify
from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required
)
from datetime import datetime, timezone
from models import USLI
from app.shared import db, uid
from models.post import Post, PostContent
from models.user_profile import UserProfile
from resources.posts.post_create.post_create_request_schema import PostCreateDataRequestSchema, PostCreateRequestSchema, PostsCreateResponseSchema
from schemas.error import ErrorSchema
from schemas.meta import MetaSchema
from app.shared import bcrypt
from app.s3 import client

blp = Blueprint("PostCreate", __name__, description="Post Create")

@blp.route("/post/create")
class PostCreate(MethodView):
    @jwt_required()
    @blp.arguments(PostCreateRequestSchema)
    @blp.response(200, PostsCreateResponseSchema)
    def post(self, request):
        data = request["data"]
        visibility = request["visibility"]
        owner_uid = get_jwt_identity()
        post_id = uid.hex
        post = Post(post_id=post_id,
                    owner_uid=owner_uid,
                    visibility=visibility,
                    type="POST",
                    original_post_id="",
                    like_count=0,
                    comment_count=0,
                    created_date_timestamp=int(datetime.now(timezone.utc).timestamp()),
                    updated_date_timestamp=int(datetime.now(timezone.utc).timestamp()))
        db.session.add(post)
        db.session.commit()
        self.handleContentList(request, post_id)
        return self.getPostsCreateResponseSchema(request)
    
    def handleContentList(self, request, post_id):
        for content in list(request["data"]):
            index = content["index"]
            text = content["text"]
            text_type = content["text_type"]
            type = content["type"]
            match type:
                case "IMAGE":
                    for image in list(content["images"]):
                        image_index = image["index"]
                        image_data = image["data"]
                        post_content = PostContent(index=image_index,
                                                   content_id=uid.hex,
                                                   post_id=post_id,
                                                   type=type,
                                                   text=image_data,
                                                   text_type=text_type)
                        db.session.add(post_content)
                        db.session.commit()
                case _:
                    post_content = PostContent(index=index,
                                               content_id=uid.hex,
                                               post_id=post_id,
                                               type=type,
                                               text=text,
                                               text_type=text_type)
                    db.session.add(post_content)
                    db.session.commit()
        pass

    def getPostsCreateResponseSchema(self, data):
        time = datetime.now(timezone.utc)

        meta = MetaSchema()
        meta.response_id = uid.hex
        meta.response_code = 1000
        meta.response_date = str(time)
        meta.response_timestamp = str(time.timestamp())
        meta.error = None

        response = PostsCreateResponseSchema()
        response.meta = meta
        response.data = data
        return response