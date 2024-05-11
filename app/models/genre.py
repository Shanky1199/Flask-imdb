from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import mongo

from bson import ObjectId


class Genre:
    def __init__(self, listed_in):
        self.listed_in = listed_in

    def to_dict(self):
        return {
            'listed_in': self.listed_in
        }

    def save(self):
        mongo.db.genre.insert_one(self.to_dict())


    
    @classmethod
    def insert_many(cls, genres):
        print(genres, 'genres')
        inserted_result = mongo.db.genre.insert_many([genre.to_dict() for genre in genres])
        return [str(genre_id) for genre_id in inserted_result.inserted_ids]
    
    @classmethod
    def insert_one(cls, genre):
        mongo.db.genre.insert_one(genre.to_dict())
        
    @classmethod
    def get_by_ids(cls, genre_ids):
        return [cls.get(genre_id) for genre_id in genre_ids]

    @classmethod
    def get(cls, genre_id):
        genre_data = mongo.db.genre.find_one({'_id': ObjectId(genre_id)})
        if genre_data:
            genre_data['_id'] = str(genre_data['_id'])  # Convert ObjectId to string
            return genre_data
        return None
        
    
