import uuid
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint
from datetime import datetime, timezone
from app.models.post import Post
from app.utils.full_post import FullPost
from app.routes.post_route.post.get_post.get_post_reponse_schema import GetPostResponseSchema
from app.schemas.reponse_schema.meta import MetaSchema
from app.schemas.request_schema.post_action_request_schema import PostActionRequestSchema

blp = Blueprint("GetPost", __name__, description="Get Post")

@blp.route("/post")
class GetPost(MethodView):
    @jwt_required(optional=True)
    @blp.arguments(PostActionRequestSchema)
    @blp.response(200, GetPostResponseSchema)
    def post(self, request):
        post_id = request["post_id"]
        post = FullPost(post_id=post_id).get_post()
        return self.__getGetPostSuccessResponse(post)
    
    def __getGetPostSuccessResponse(self, post: Post):
        time = datetime.now(timezone.utc)

        meta = MetaSchema()
        meta.response_id = uuid.uuid4().hex
        meta.response_code = 1000
        meta.response_date = str(time)
        meta.response_timestamp = str(time.timestamp())
        meta.error = None

        response = GetPostResponseSchema()
        response.meta = meta
        response.data = post
        return response