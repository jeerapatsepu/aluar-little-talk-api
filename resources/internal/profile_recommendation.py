import os
import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint
from datetime import datetime, timezone
from models.post.post import PostContent
from models.profile.user_profile import UserProfile
from models.profile_recommendations import ProfileRecommendation
from resources.manager.image_manager import ImageManager
from schemas.reponse_schema.meta import MetaSchema
from schemas.reponse_schema.post.post_action_response_schema import PostActionResponseSchema
from app.shared import db

blp = Blueprint("InternalProfileRecommendation", __name__, description="Internal Profile Recommendation")

@blp.route("/internal/profile/recommendation")
class InternalProfileRecommendation(MethodView):
    @blp.response(200, PostActionResponseSchema)
    def post(self):
        internal_header_key = request.headers.get("X-Internal-Auth")
        if internal_header_key == os.getenv("INTERNAL_AUTH_KEY"):
            self.__delete_profile()
            self.__check_profile_list()
            return self.__getSuccessResponse()
        else:
            return self.__getFailResponse()
    
    def __delete_profile(self):
        profile_recommendation_list = ProfileRecommendation.query.all()
        for profile_recommendation in profile_recommendation_list:
            profile = UserProfile.query.filter(UserProfile.uid == profile_recommendation.user_id).first()
            verify_photo = ImageManager(profile.photo).verify_profile_photo()
            content_list = PostContent.query.filter_by(owner_uid=profile.uid).all()
            verify_content = len(list(filter(lambda x: len(x.text) >= 255, content_list))) > 5
            if profile and not verify_photo or not verify_content:
                db.session.delete(profile_recommendation)
                db.session.commit()

    def __check_profile_list(self):
        profile_list = UserProfile.query.order_by(UserProfile.photo).filter(UserProfile.photo.contains("https://")).all()
        now = int(datetime.now(timezone.utc).timestamp())
        for profile in profile_list:
            verify_photo = ImageManager(profile.photo).verify_profile_photo()
            content_list = PostContent.query.filter_by(owner_uid=profile.uid).all()
            verify_content = len(list(filter(lambda x: len(x.text) >= 255, content_list))) > 5
            profile_in_recommendation = ProfileRecommendation.query.filter(ProfileRecommendation.user_id == profile.uid).first()
            if profile_in_recommendation:
                db.session.delete(profile_in_recommendation)
                db.session.commit()
            if verify_photo and verify_content:
                recommend_profile = ProfileRecommendation(user_id=profile.uid, created_date_timestamp=now)
                db.session.add(recommend_profile)
                db.session.commit()

    def __getSuccessResponse(self):
        time = datetime.now(timezone.utc)

        meta = MetaSchema()
        meta.response_id = uuid.uuid4().hex
        meta.response_code = 1000
        meta.response_date = str(time)
        meta.response_timestamp = str(time.timestamp())
        meta.error = None

        response = PostActionResponseSchema()
        response.meta = meta
        return response
    
    def __getFailResponse(self):
        time = datetime.now(timezone.utc)

        meta = MetaSchema()
        meta.response_id = uuid.uuid4().hex
        meta.response_code = 5000
        meta.response_date = str(time)
        meta.response_timestamp = str(time.timestamp())
        meta.error = None

        response = PostActionResponseSchema()
        response.meta = meta
        return response