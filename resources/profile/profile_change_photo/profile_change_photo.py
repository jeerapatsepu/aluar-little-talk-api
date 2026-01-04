import base64
import os
import uuid
from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required, current_user
from datetime import datetime, timezone
from models.profile.user_profile import UserProfile
from app.shared import db
from resources.base.profile import ProfileBase
from resources.profile.profile_change_photo.profile_change_photo_schema import ProfileChangePhotoRequestSchema, ProfileChangePhotoResponseSchema
from schemas.reponse_schema.meta import MetaSchema
from app.s3 import client

blp = Blueprint("ProfileChangePhoto", __name__, description="Profile Change Photo")

@blp.route("/profile/change_photo")
class ProfileChangePhoto(MethodView):
    @jwt_required()
    @blp.arguments(ProfileChangePhotoRequestSchema)
    @blp.response(200, ProfileChangePhotoResponseSchema)
    def post(self, request):
        image = request["image"]
        profile = UserProfile.query.filter_by(uid=current_user.uid).one()
        self.__deleteProfilePhoto()
        image_path = self.__upload_photo(image_data=image)
        profile.photo = image_path
        db.session.commit()
        return self.__getSuccessResponse(uid=current_user.uid)
    
    def __deleteProfilePhoto(self):
        try: 
            bucket = os.getenv("S3_BUCKET_NAME")
            prefix = "photos/" + current_user.uid
            response = client.list_objects_v2(
                Bucket=bucket,
                Prefix=prefix
            )
            if "Contents" in response:
                client.delete_objects(
                    Bucket=bucket,
                    Delete={
                        "Objects": [{"Key": obj["Key"]} for obj in response["Contents"]]
                    }
                )
        except Exception:
            pass

    def __upload_photo(self, image_data: str):
        image_path = 'photos/' + current_user.uid + '/' + current_user.uid + '.jpg'
        client.put_object(Body=base64.b64decode(image_data),
                            Bucket=os.getenv("S3_BUCKET_NAME"),
                            Key=image_path,
                            ACL='public-read',
                            ContentType='image/jpeg')
        image_url=os.getenv('LITTLE_TALK_S3_ENDPOINT') + '/' + image_path
        return image_url

    def __getSuccessResponse(self, uid: str):
        time = datetime.now(timezone.utc)

        meta = MetaSchema()
        meta.response_id = uuid.uuid4().hex
        meta.response_code = 1000
        meta.response_date = str(time)
        meta.response_timestamp = str(time.timestamp())
        meta.error = None

        data = ProfileBase(uid=uid).get_ProfileDataResponseSchema()

        response = ProfileChangePhotoResponseSchema()
        response.meta = meta
        response.data = data
        return response