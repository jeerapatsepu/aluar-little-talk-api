
from datetime import datetime, timedelta
from models.post.post import Post
from models.profile.user_profile import UserProfile
from models.profile.user_relationship import UserRelationship
from models.user_delete_request import UserDeleteRequest
from models.usli import USLI
from resources.full_post import FullPost

def __deleteUserThan15Days():
        user_uid_list = UserDeleteRequest.query.filter_by(__isThan15Days(created_date_timestamp=credits)).all()
        for uid in user_uid_list:
            USLI.query.filter_by(uid=uid).delete()
            UserProfile.query.filter_by(uid=uid).delete()
            UserRelationship.query.filter_by(sender_id=uid).delete()
            UserRelationship.query.filter_by(receiver_id=uid).delete()
            UserDeleteRequest.query.filter_by(user_uid=uid).delete()
            post_list = Post.query.filter_by(owner_uid=uid).all()
            for post in post_list:
                FullPost(post_id=post.post_id, owner_uid=uid).delete_post()

def __isThan15Days(created_date_timestamp: int) -> bool:
    ts_date = datetime.fromtimestamp(created_date_timestamp)
    return datetime.now() - ts_date > timedelta(days=15)

if __name__ == "__main__":
    __deleteUserThan15Days()