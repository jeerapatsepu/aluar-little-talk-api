import logging
from flask_jwt_extended import current_user
from models.profile.user_profile import UserProfile
from models.profile.user_relationship import UserRelationship
from schemas.reponse_schema.profile.profile_data_response_schema import ProfileDataResponseSchema

class ProfileBase:
    def __init__(self, uid: str):
        self.__uid = uid
    
    def get_ProfileDataResponseSchema(self):
        profile = UserProfile.query.filter_by(uid=self.__uid).first()
        data = ProfileDataResponseSchema()
        data.name = profile.full_name
        data.uid = profile.uid
        data.photo = profile.photo
        data.caption = profile.caption
        data.link = profile.link
        data.email = profile.email
        try:
            relationship_status_of_current_user = UserRelationship.query.filter_by(sender_id=current_user.uid, receiver_id=profile.uid).first() ## bb -> jee
            relationship_status_of_user = UserRelationship.query.filter_by(sender_id=profile.uid, receiver_id=current_user.uid).first() # jee -> bb
            relationship_status = ""
            if relationship_status_of_current_user and relationship_status_of_current_user.status == "FOLLOW":
                relationship_status = "FOLLOW"
            if relationship_status_of_user and relationship_status_of_user.status == "FOLLOW" and relationship_status_of_current_user and relationship_status_of_current_user.status == "FOLLOW":
                relationship_status = "FRIEND"
            data.relationship_status = relationship_status
            data.follower_count = UserRelationship.query.filter_by(receiver_id=current_user.uid).count()
            data.following_count = UserRelationship.query.filter_by(sender_id=current_user.uid).count()
        except Exception:
            # logging.exception(Exception)
            data.relationship_status = None
        return data
    