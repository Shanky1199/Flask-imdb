from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import mongo

class User(UserMixin):
    def __init__(self, username, password):
        self.username = username
        print('generating password hash of', str(password), generate_password_hash(str(password)))
        self.password_hash = generate_password_hash(str(password))
    
    @classmethod
    def get(cls, username):
        user_data = mongo.db.users.find_one({"username": username})
        if not user_data:
            return None
        user = cls(username=user_data['username'], password=user_data['password'])
        user.id = str(user_data['_id'])
        return user
    
    def save(self):
        mongo.db.users.insert_one({"username": self.username, "password": self.password_hash})
    
    def check_password(self, password):
        print(self.password_hash, password)
        return check_password_hash(self.password_hash, password)
