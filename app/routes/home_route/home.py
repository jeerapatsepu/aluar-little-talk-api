from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required
from app.services.home_service import get_home_feed
from app.utils.resposne_helper import get_meta_sucess_response
from app.schemas.reponse_schema.profile_posts_response import ProfilePostsResponseSchema
from app.schemas.request_schema.home_feed_request_schema import HomeFeedRequestSchema

blp = Blueprint("Home", __name__, description="Home")

@blp.route("/home/feed")
class Home(MethodView):
    @jwt_required(optional=True)
    @blp.arguments(HomeFeedRequestSchema)
    @blp.response(200, ProfilePostsResponseSchema)
    def post(self, request):
        post_list = get_home_feed(request)
        return self.__get_success_response(post_list)

    def __get_success_response(self, data):
        response = ProfilePostsResponseSchema()
        response.meta = get_meta_sucess_response()
        response.data = data
        return response