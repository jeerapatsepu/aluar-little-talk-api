from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import (
    current_user,
    jwt_required
)
from datetime import datetime, timezone
from app.shared import db, uid
from models.post import Post, PostContent, PostImageContent
from models.post_bookmark_model import PostBookmarkModel
from models.post_like_model import PostLikeModel
from models.post_repost_model import PostRepostModel
from models.user_profile import UserProfile
from resources.posts.post_create.post_create_request_schema import PostCreateDataImageRequestSchema
from resources.profile.posts.profile_posts.posts_request_schema import ProfilePostsDataResponseSchema, ProfilePostsRequestSchema, ProfilePostsResponseSchema
from schemas.meta import MetaSchema

blp = Blueprint("ProfilePosts", __name__, description="Profile Posts")

@blp.route("/profile/posts")
class ProfilePosts(MethodView):
    @jwt_required(optional=True)
    @blp.arguments(ProfilePostsRequestSchema)
    @blp.response(200, ProfilePostsResponseSchema)
    def post(self, request):
        uid = request["uid"]
        offset = request["offset"]
        limit = request["limit"]
        posts = Post.query.filter_by(owner_uid=uid).offset(offset).limit(limit).all()
        posts.sort(key=self.sortPostsList, reverse=True)
        profile = UserProfile.query.filter_by(uid=uid).first()
        new_posts = self.getContentListEachPost(profile, posts)
        return self.getPofilePostsSuccessResponse(new_posts)

    def sortPostsList(self, e):
        return e.created_date_timestamp

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
            try:
                like = PostLikeModel.query.filter_by(post_id=post.post_id, user_uid=current_user.uid).first()
                if like:
                    post.is_like = True
                bookmark = PostBookmarkModel.query.filter_by(post_id=post.post_id, user_uid=current_user.uid).first()
                if bookmark:
                    post.is_bookmark = True
                repost = PostRepostModel.query.filter_by(post_id=post.post_id, user_uid=current_user.uid).first()
                if repost:
                    post.is_repost = True
            except Exception:
                post.is_like = None
                post.is_bookmark = None
                post.is_repost = None
            post.like_count = PostLikeModel.query.filter_by(post_id=post.post_id).count()
            if like:
                post.is_like = True
        return post_list
    
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