class PostModelHelper:
    @staticmethod
    def get_post_by_id(post_id: str):
        return Post.query.filter(Post.post_id == post_id).first()