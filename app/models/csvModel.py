from app.extensions import mongo
class CSVModel:
    @classmethod
    def upload_csv(cls, filename, total_records):
        upload_data = {
            'filename': filename,
            'progress': 0,  # Initial progress
            'total_records': total_records  # Initialize total records count
        }
        mongo.db.uploads_collection.insert_one(upload_data)

    @classmethod
    def update_progress(cls, filename, progress):
        mongo.db.uploads_collection.update_one(
            {'filename': filename},
            {'$set': {'progress': progress}}
        )

    @classmethod
    def get_progress(cls, filename):
        return mongo.db.uploads_collection.find_one({'filename': filename}, {'_id': 0, 'progress': 1})