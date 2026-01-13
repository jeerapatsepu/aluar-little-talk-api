from app.shared import db

class ProfileRecommendation(db.Model):
    __tablename__ = "profile_recommendations"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String)
    created_date_timestamp = db.Column(db.Integer)