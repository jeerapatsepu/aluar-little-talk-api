from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import current_user, jwt_required
from datetime import datetime, timezone
import uuid
from app.shared import db
from models.post.post import Post, PostContent, PostImageContent
from resources.base.post.post_create.post_create_response_schema import PostsCreateResponseSchema
from schemas.reponse_schema.meta import MetaSchema
from app.s3 import client
import base64
import os
from schemas.reponse_schema.meta import MetaSchema
from schemas.request_schema.post.post_create_request_schema import PostCreateRequestSchema

blp = Blueprint("PostCreate", __name__, description="Post Create")

@blp.route("/post/create")
class PostCreate(MethodView):
    @jwt_required()
    @blp.arguments(PostCreateRequestSchema)
    @blp.response(200, PostsCreateResponseSchema)
    def post(self, request):
        self.__createPost(request=request)
        return self.__getPostsCreateResponseSchema(request)
    
    def __createPost(self, request):
        data = request["data"]
        visibility = request["visibility"]
        post_id = uuid.uuid4().hex
        owner_uid = current_user.uid
        post = Post(post_id=post_id,
                    owner_uid=owner_uid,
                    visibility=visibility,
                    type="POST",
                    original_post_id="",
                    created_date_timestamp=int(datetime.now(timezone.utc).timestamp()),
                    updated_date_timestamp=int(datetime.now(timezone.utc).timestamp()))
        db.session.add(post)
        db.session.commit()
        self.__createContent(request, post_id)

    def __createContent(self, request, post_id):
        for content in list(request["data"]):
            index = content["index"]
            text = content["text"]
            text_type = content["text_type"]
            type = content["type"]
            images = content["images"]
            match type:
                case "IMAGE":
                    content = PostContent(index=index,
                                               content_id=uuid.uuid4().hex,
                                               post_id=post_id,
                                               type=type,
                                               text=text,
                                               text_type=text_type,
                                               owner_uid=current_user.uid)
                    db.session.add(content)
                    db.session.commit()
                    self.__createImageContent(post_id, content, list(images))
                case _:
                    post_content = PostContent(index=index,
                                               content_id=uuid.uuid4().hex,
                                               post_id=post_id,
                                               type=type,
                                               text=text,
                                               text_type=text_type,
                                               owner_uid=current_user.uid)
                    db.session.add(post_content)
                    db.session.commit()
    
    def __createImageContent(self, post_id, content: PostContent, content_image_list: list):
        for image in content_image_list:
            image_content_id = uuid.uuid4().hex
            image_path = 'posts/' + post_id + '/' + content.content_id + '/' + image_content_id + '.jpg'
            client.put_object(Body=base64.b64decode(str(image["data"])),
                              Bucket=os.getenv("S3_BUCKET_NAME"),
                              Key=image_path,
                              ACL='public-read',
                              ContentType='image/jpeg')
            image_url=os.getenv('LITTLE_TALK_S3_ENDPOINT') + '/' + image_path
            image_content = PostImageContent(index=image["index"],
                                             post_id=post_id,
                                             content_id=content.content_id,
                                             image_content_id=image_content_id,
                                             link=image_url,
                                             owner_uid=current_user.uid)
            
            db.session.add(image_content)
            db.session.commit()

    def __getPostsCreateResponseSchema(self, data):
        time = datetime.now(timezone.utc)

        meta = MetaSchema()
        meta.response_id = uuid.uuid4().hex
        meta.response_code = 1000
        meta.response_date = str(time)
        meta.response_timestamp = str(time.timestamp())
        meta.error = None

        response = PostsCreateResponseSchema()
        response.meta = meta
        response.data = data
        return response