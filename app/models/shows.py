from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import mongo

class Shows:
    def __init__(self, show):
        self.show_id = show['show_id']
        self.title = show['title']
        self.type = show['type']
        self.description = show['description']
        self.duration = show['duration']
        self.cast_ids = show['cast_ids']  # Assuming cast_ids is a list of cast MongoDB IDs
        self.genre_ids = show['genre_ids']  # Assuming genre_ids is a list of genre MongoDB IDs
        self.ratings_id = show['ratings_id']  # Assuming ratings_id is the ratings MongoDB ID

    def to_dict(self):
        return {
            'show_id': self.show_id,
            'title': self.title,
            'type': self.type,
            'description': self.description,
            'duration': self.duration,
            'cast_ids': self.cast_ids,
            'genre_ids': self.genre_ids,
            'ratings_id': self.ratings_id
        }
        
    def save(self):
        mongo.db.shows.insert_one(self.to_dict())

    @classmethod
    def get(cls, show_id):
        return mongo.db.shows.find_one({'show_id': show_id})
    
    @classmethod
    def get_all(cls, page=1, page_size=10, sort_key='date_added'):
        skip = (page - 1) * page_size
        print('coming till here')
        shows = mongo.db.shows.find().sort(sort_key).skip(skip).limit(page_size)
        return [cls(show) for show in shows]
    
    @classmethod
    def insert_many(cls, shows):
        mongo.db.shows.insert_many([show.to_dict() for show in shows])

    @classmethod
    def insert_one(cls, show):
        mongo.db.shows.insert_one(show.to_dict())
