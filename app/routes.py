from flask import jsonify, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.extensions import login_manager
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from app.models.user import User
from app.models.shows import Shows
from app.models.cast import Cast
from app.models.genre import Genre
from app.models.ratings import Ratings
from app.models.csvModel import CSVModel
from werkzeug.utils import secure_filename
from datetime import datetime
import pandas as pd
import json

# Setup login manager user loader
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

def init_app(app):
    @app.route('/')
    def index():
        return "Hello World!"

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid JSON request'}), 400

        username = data.get('username')
        password = data.get('password')
        if not username or not password:
            return jsonify({'error': 'Missing username or password'}), 400

        user = User.get(username)
        if user and user.check_password(password):
            access_token = create_access_token(identity=user.id)
            login_user(user)
            return jsonify({'access_token': access_token}), 200
        else:
            return jsonify({'error': 'Invalid username or password'}), 401

    @app.route('/dashboard')
    @login_required
    def dashboard():
        # Ensure dashboard.html exists in the templates folder
        return render_template('dashboard.html', username=current_user.username)

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('index'))

    @app.route('/create_user', methods=['POST'])
    def create_user():
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No input data provided'}), 400
        username = data.get('username')
        password = data.get('password')

        # Basic validation
        if not username or not password:
            return jsonify({'error': 'Missing username or password'}), 400

        # Check if user already exists
        if User.get(username) is not None:
            return jsonify({'error': 'User already exists'}), 409  # Use 409 Conflict for duplicates

        # Create new user
        new_user = User(username, password)
        new_user.save()

        return jsonify({'success': 'User created successfully'}), 201
    
    
    @app.route('/api/upload-csv', methods=['POST'])
    @jwt_required()
    def upload_csv():
        try:
            
            if 'file' not in request.files:
                return jsonify({'error': 'No file provided'}), 400
            file = request.files['file']
            if file.filename == '':
                return jsonify({'error': 'No selected file'}), 400
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                data_frame = pd.read_csv(file)
                records = data_frame.to_dict(orient='records')
                total_records = len(records)
            else:
                return jsonify({'error': 'Invalid file type'}), 400
            
            CSVModel.upload_csv(filename, total_records)
            for idx, record in enumerate(records):
                combined_record = parse_movie_data(record)
                save_combined_record(combined_record)
                progress = int((idx + 1) / total_records * 100)
                print(current_user, "current user")
                CSVModel.update_progress(filename, progress)
        
            return jsonify({'message': 'Data saved successfully'})
        except Exception as e:
            print(f"Error in uploading CSV: {e}")
            return jsonify({'error': 'An error occurred while processing the file'}), 500
    
    @app.route('/api/shows', methods=['GET'])
    @jwt_required()
    def get_shows():
        page = int(request.args.get('page', 1))  # Default page number is 1
        page_size = int(request.args.get('page_size', 10))  # Default page size is 10
        sort_by = request.args.get('sort_by', 'date_added')  # Default sort by date_added

        # Determine the sort key based on the requested sort_by parameter
        sort_key = 'date_added' if sort_by == 'date_added' else 'release_date' if sort_by == 'release_date' else 'duration'

        # Fetch shows based on pagination and sorting
        shows = Shows.get_all(page=page, page_size=page_size, sort_key=sort_key)

        # Convert shows to dictionary format
        shows_list = [show.to_dict() for show in shows]

        for show in shows_list:
            show['cast'] = [cast for cast in Cast.get_by_ids(show['cast_ids'])]
            show['genre'] = [genre for genre in Genre.get_by_ids(show['genre_ids'])]
            show['ratings'] = Ratings.get(show['ratings_id'])
            show.pop('cast_ids', None)
            show.pop('ratings_id', None)
            show.pop('genre_ids', None)
            
        

        return jsonify({'shows': shows_list})
    
    @app.route('/api/upload-progress', methods=['GET'])
    @jwt_required()
    def get_upload_progress():
        progress = CSVModel.get_progress(current_user.id)
        if progress:
            return jsonify({'progress': progress['progress']})
        else:
            return jsonify({'error': 'Progress not available'})
            
    

    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'csv'}
    
    def save_combined_record(combined_record):
        shows, cast, genre, ratings = combined_record.values()

        # Save cast, genre, and ratings first to get their MongoDB _ids
        cast_ids = save_casts(cast) if cast else []
        genre_ids = save_genres(genre)
        ratings_id = save_ratings(ratings) if ratings else None

        # Update the show data with the MongoDB _ids
        shows['cast_ids'] = cast_ids
        shows['genre_ids'] = genre_ids
        shows['ratings_id'] = ratings_id

        # Save the updated show data
        save_shows(shows)

    def save_casts(cast):
        if not cast:
            return []

        cast_objects = [Cast(c) for c in cast]
        insertIds = Cast.insert_many(cast_objects)
        print(insertIds, 'insertedids')
        return insertIds

    def save_genres(genre):
        genre_objects = [Genre(g) for g in genre]
        insertedIds = Genre.insert_many(genre_objects)
        return insertedIds

    def save_ratings(ratings):
        if not ratings:
            return None

        ratings_obj = Ratings(ratings)
        insertedIds = Ratings.insert_one(ratings_obj)
        return insertedIds

    def save_shows(shows):
        new_show = Shows(shows)
        new_show.save()
    
    def parse_movie_data(movie_data):
        # Extract data from the JSON object
        show_id = movie_data['show_id']
        title = movie_data['title']
        type = movie_data['type']
        
        # Check and set 'director' to 'N/A' if missing or empty
        director = movie_data['director'] if movie_data['director'] else 'N/A'
        
        # Check if 'cast' is a string, otherwise default to an empty string
        cast_str = str(movie_data.get('cast', ''))
        cast_list = cast_str.split(', ') if cast_str else []  # Split if 'cast' is a non-empty string
        country = movie_data['country']
        
        # Check and convert 'date_added' format
        date_added_str = movie_data.get('date_added', '')
        date_added = datetime.strptime(date_added_str, "%B %d, %Y") if date_added_str else None
        
        release_year = movie_data['release_year']
        rating = movie_data['rating']
        duration = movie_data['duration']
        listed_in = movie_data['listed_in']
        description = movie_data['description']

        # Create JSON objects for Shows, Cast, Genre, and Ratings
        shows_json = {
            'show_id': show_id,
            'title': title,
            'type': type,
            'description': description,
            'duration': duration
        }

        cast_json = [{'show_id': show_id, 'cast': actor, 'director': director} for actor in cast_list]

        genre_list = listed_in.split(', ')
        genre_json = {'genres': genre_list}

        ratings_json = {
            'show_id': show_id,
            'release_year': release_year,
            'rating': rating,
            'country': country
        }

        # Combine JSON objects into a single response
        combined_json = {
            'shows': shows_json,
            'cast': cast_json,
            'genre': genre_json,
            'ratings': ratings_json
        }

        return combined_json