from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity
from flask_smorest import Blueprint
from datetime import datetime, timezone
from app.shared import uid
from models.post import Post, PostContent, PostImageContent
from models.post_like_model import PostLikeModel
from models.user_profile import UserProfile
from resources.posts.get_post.get_post_request_schema import GetPostRequestSchema, GetPostResponseSchema
from resources.posts.post_create.post_create_request_schema import PostCreateDataImageRequestSchema
from schemas.meta import MetaSchema

blp = Blueprint("GetPost", __name__, description="Get Post")

@blp.route("/post")
class GetPost(MethodView):
    @blp.arguments(GetPostRequestSchema)
    @blp.response(200, GetPostResponseSchema)
    def post(self, request):
        post_id = request["post_id"]
        owner_uid = get_jwt_identity()
        post = Post.query.filter_by(post_id=post_id).one()
        profile = UserProfile.query.filter_by(uid=owner_uid).first()
        if post:
            new_post = self.getContentListEachPost(profile, post)
            return self.getPofilePostsSuccessResponse(new_post)
        return self.getPofilePostsSuccessResponse(None)

    def getContentListEachPost(self, profile: UserProfile, post: Post):
        if profile:
            post.owner_name = profile.full_name
            post.owner_image = profile.photo
        post_contents = PostContent.query.filter_by(post_id=post.post_id).all()
        post_contents.sort(key=self.sortList)
        post.is_see_more = False
        if len(post_contents) > 2:
            post_contents.pop()
            post.is_see_more = True
        post.contents = self.getImageContentEachContent(post_contents)
        post.is_like = False
        like = PostLikeModel.query.filter_by(post_id=post.post_id, user_uid=profile.uid).first()
        post.like_count = PostLikeModel.query.filter_by(post_id=post.post_id).count()
        if like:
            post.is_like = True
        return post
    
    def getImageContentEachContent(self, content_list: list):
        for content in content_list:
            if content.type == "IMAGE":
                image_list = PostImageContent.query.filter_by(content_id=content.content_id).all()
                image_list.sort(key=self.sortList)
                image_respone_list = []
                for image in image_list:
                    image_response = PostCreateDataImageRequestSchema()
                    image_response.index = image.index
                    image_response.data = image.link
                    image_respone_list.append(image_response)
                content.images = image_respone_list
        return content_list

    def sortList(self, e):
        return e.index
    
    def getPofilePostsSuccessResponse(self, post):
        time = datetime.now(timezone.utc)

        meta = MetaSchema()
        meta.response_id = uid.hex
        meta.response_code = 1000
        meta.response_date = str(time)
        meta.response_timestamp = str(time.timestamp())
        meta.error = None

        response = GetPostResponseSchema()
        response.meta = meta
        response.data = post
        return response