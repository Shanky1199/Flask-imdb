from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import mongo

from bson import ObjectId

class Cast:
    def __init__(self, cast):
        self.show_id = cast['show_id']
        self.cast = cast['cast']
        self.director = cast['director']

    def to_dict(self):
        return {
            'show_id': self.show_id,
            'cast': self.cast,
            'director': self.director
        }

    def save(self):
        mongo.db.cast.insert_one(self.to_dict())


    @classmethod
    def insert_many(cls, casts):
        inserted_result = mongo.db.cast.insert_many([cast.to_dict() for cast in casts])
        return [str(cast_id) for cast_id in inserted_result.inserted_ids]

    @classmethod
    def insert_one(cls, cast):
        mongo.db.cast.insert_one(cast.to_dict())
    
    @classmethod
    def get_by_ids(cls, cast_ids):
        return [cls.get(cast_id) for cast_id in cast_ids]
    
    @classmethod
    def get_by_ids(cls, cast_ids):
        return [cls.get(cast_id) for cast_id in cast_ids]

    @classmethod
    def get(cls, cast_id):
        cast_data = mongo.db.cast.find_one({'_id': ObjectId(cast_id)})
        if cast_data:
            cast_data['_id'] = str(cast_data['_id'])  # Convert ObjectId to string
            return cast_data
        return None
