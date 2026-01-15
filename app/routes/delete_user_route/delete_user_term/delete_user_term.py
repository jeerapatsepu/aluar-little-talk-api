import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint
from datetime import datetime, timezone
from app.routes.delete_user_route.delete_user_term.delete_user_term_schema import DeleteUserTermDataSchema, DeleteUserTermResponseSchema
from app.schemas.request_schema.profile_change_photo_schema import ProfileChangePhotoResponseSchema
from app.schemas.reponse_schema.meta import MetaSchema

blp = Blueprint("DeleteUserTerm", __name__, description="Delete User Term")

@blp.route("/delete/user/term")
class DeleteUserTerm(MethodView):
    @blp.response(200, DeleteUserTermResponseSchema)
    def get(self):
        language = request.headers.get("Language")
        if language == "th":
            return self.__getTermTH()
        else:
            return self.__getTermEN()
    
    def __getTermTH(self):
        data = DeleteUserTermDataSchema()
        data.title = "การลบบัญชีผู้ใช้"
        data.description = "ผู้ใช้สามารถยื่นคำขอลบบัญชีผู้ใช้ได้ตลอดเวลา เมื่อผู้ใช้ส่งคำขอลบแล้ว \
                            ระบบจะเริ่มกระบวนการลบบัญชีภายในระยะเวลา \
                            15 (สิบห้า) วัน นับจากวันที่ระบบได้รับคำขอ\
                            \
                            ในระหว่างระยะเวลาดังกล่าว ผู้ใช้สามารถยกเลิกคำขอลบบัญชีได้\
                            หากครบกำหนดระยะเวลา 15 วันโดยไม่มีการยกเลิกคำขอ\
                            บัญชีผู้ใช้ รวมถึงข้อมูลส่วนบุคคล เนื้อหา และข้อมูลที่เกี่ยวข้องทั้งหมด\
                            จะถูกลบออกจากระบบอย่างถาวร และไม่สามารถกู้คืนได้ไม่ว่ากรณีใด ๆ\
                            \
                            ทั้งนี้ อาจเก็บรักษาข้อมูลบางส่วนไว้เท่าที่จำเป็น\
                            เพื่อปฏิบัติตามกฎหมาย ข้อบังคับ\
                            หรือเพื่อการใช้สิทธิและการป้องกันสิทธิทางกฎหมาย"
        return self.__getSuccessResponse(data=data)
    
    def __getTermEN(self):
        data = DeleteUserTermDataSchema()
        data.title = "Account Deletion"
        data.description = "Users may request account deletion at any time.\
                            Once a deletion request is submitted, the account will be scheduled for deletion\
                            within 15 (fifteen) days from the date the request is recorded by the system.\
                            \
                            During this period, users may cancel the deletion request.\
                            If the request is not canceled within the 15-day period,\
                            the account, including all personal data, content, and related information,\
                            will be permanently deleted and cannot be recovered under any circumstances.\
                            \
                            Notwithstanding the foregoing, may retain certain information\
                            as required by applicable laws, regulations,\
                            or for the establishment, exercise, or defense of legal claims."
        return self.__getSuccessResponse(data=data)
    
    def __getSuccessResponse(self, data: DeleteUserTermDataSchema):
        time = datetime.now(timezone.utc)

        meta = MetaSchema()
        meta.response_id = uuid.uuid4().hex
        meta.response_code = 1000
        meta.response_date = str(time)
        meta.response_timestamp = str(time.timestamp())
        meta.error = None

        response = ProfileChangePhotoResponseSchema()
        response.meta = meta
        response.data = data
        return response