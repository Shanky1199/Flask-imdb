from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import mongo


from bson import ObjectId

class Ratings:
    def __init__(self, ratings):
        self.show_id = ratings['show_id']
        self.release_year = ratings['release_year']
        self.rating = ratings['rating']
        self.country = ratings['country']

    def to_dict(self):
        return {
            'show_id': self.show_id,
            'release_year': self.release_year,
            'rating': self.rating,
            'country': self.country
        }

    def save(self):
        mongo.db.ratings.insert_one(self.to_dict())

    @classmethod
    def get(cls, ratings_id):
        ratings_data = mongo.db.ratings.find_one({'_id': ObjectId(ratings_id)})
        if ratings_data:
            ratings_data['_id'] = str(ratings_data['_id'])  # Convert ObjectId to string
            return ratings_data
        return None
    
    @classmethod
    def insert_many(cls, ratings):
       inserted_result = mongo.db.ratings.insert_many([ratings.to_dict() for rating in ratings])
       return [str(cast_id) for cast_id in inserted_result.inserted_ids]

    @classmethod
    def get_by_ids(cls, cast_ids):
        return [cls.get(cast_id) for cast_id in cast_ids]
    
    @classmethod
    def insert_one(cls, rating):
        mongo.db.ratings.insert_one(rating.to_dict())
        
    
