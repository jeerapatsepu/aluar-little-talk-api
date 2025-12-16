from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import (
    jwt_required
)
from datetime import datetime, timezone
from app.shared import db, uid
from models.post import Post, PostContent, PostImageContent
from models.user_profile import UserProfile
from resources.profile.posts.profile_posts.posts_request_schema import ProfilePostsDataResponseSchema, ProfilePostsRequestSchema, ProfilePostsResponseSchema
from schemas.meta import MetaSchema

blp = Blueprint("ProfilePosts", __name__, description="Profile Posts")

@blp.route("/profile/posts")
class ProfilePosts(MethodView):
    @jwt_required()
    @blp.arguments(ProfilePostsRequestSchema)
    @blp.response(200, ProfilePostsResponseSchema)
    def post(self, request):
        uid = request["uid"]
        offset = request["offset"]
        limit = request["limit"]
        posts = Post.query.filter_by(owner_uid=uid).offset(offset).limit(limit).all()
        profile = UserProfile.query.filter_by(uid=uid).first()
        new_posts = self.getContentListEachPost(profile, posts)
        return self.getPofilePostsSuccessResponse(new_posts)

    def getContentListEachPost(self, profile: UserProfile, post_list: list):
        for post in post_list:
            if profile:
                post.owner_name = profile.full_name
                post.owner_image = profile.photo
            post_contents = PostContent.query.filter_by(post_id=post.post_id).offset(0).limit(3).all()
            post_contents.sort(key=self.sortList)
            post.is_see_more = False
            if len(post_contents) > 2:
                post_contents.pop()
                post.is_see_more = True
            post.contents = self.getImageContentEachContent(post_contents)
        return post_list
    
    def getImageContentEachContent(self, content_list: list):
        for content in content_list:
            if content.type == "IMAGE":
                image_list = PostImageContent.query.filter_by(content_id=content.content_id).all()
                image_list.sort(key=self.sortList)
                content.images = image_list
        return content_list

    def sortList(self, e):
        return e.index
    
    def getPofilePostsSuccessResponse(self, posts):
        time = datetime.now(timezone.utc)

        meta = MetaSchema()
        meta.response_id = uid.hex
        meta.response_code = 1000
        meta.response_date = str(time)
        meta.response_timestamp = str(time.timestamp())
        meta.error = None

        response = ProfilePostsResponseSchema()
        response.meta = meta
        response.data = posts
        return response