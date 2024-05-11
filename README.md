
# Project Name
# Flask-imdb

## Overview

You are working as an engineer for IMDB the world's most popular and authoritative source for movie, TV and celebrity content.

## Setup

After Cloning from Git 
Run 2 commands

1 make venv - this will make your virtual environment

2. make server - to run server

## API Documentation

### Authentication

Before accessing the protected endpoints, you need to authenticate and obtain an access token. Use the `/login` endpoint to log in and receive an access token.

#### Login

- **URL:** `/login`
- **Method:** `POST`
- **Request Body:**
  ```json
  {
      "username": "your_username",
      "password": "your_password"
  }


# Endpoints

## Upload CSV

Upload a CSV file.

- **URL:** `/api/upload-csv`
- **Method:** `POST`
- **Authorization:** Bearer Token (Access Token)
- **Request Body:** Form Data with file field
- **Response:** 
  - Success: `{ "message": "Data saved successfully" }`
  - Error: `{ "error": "Error message" }`

## Get Shows

Retrieve shows data.

- **URL:** `/api/shows`
- **Method:** `GET`
- **Authorization:** Bearer Token (Access Token)
- **Query Parameters:**
  - `page`: Page number (default: 1)
  - `page_size`: Number of items per page (default: 10)
  - `sort_by`: Sort parameter (e.g., date_added, release_date, duration)


## CSV Progress

Retrieve upload progress for a CSV file.

- **URL:** `/api/upload-progress`
- **Method:** `GET`
- **Authorization:** Bearer Token (Access Token)
- **Response:** 
  - Success: `{ "progress": 50 }` (Example progress value)
  - Error: `{ "error": "Progress not available" }`


## DB schema examples

``` json
{
    "uploads_collections": {
        "indexes": [],
        "schema": {
            "_id": {"type": "ObjectId"},
            "filename": {"type": "str"},
            "progress": {"type": "int"},
            "total_records": {"type": "int"}
        }
    },
    "Genre": {
        "indexes": [],
        "schema": {
            "_id": {"type": "ObjectId"},
            "listed_in": {"type": "str"}
        }
    },
    "Cast": {
        "indexes": [],
        "schema": {
            "_id": {"type": "ObjectId"},
            "show_id": {"type": "str"},
            "cast": {"type": "str"},
            "director": {"type": "str"}
        }
    },
    "Ratings": {
        "indexes": [],
        "schema": {
            "_id": {"type": "ObjectId"},
            "show_id": {"type": "str"},
            "release_year": {"type": "int"},
            "rating": {"type": "str"},
            "country": {"type": "str"}
        }
    },
    "Users": {
        "indexes": [],
        "schema": {
            "_id": {"type": "ObjectId"},
            "username": {"type": "str"},
            "password": {"type": "str"}
        }
    },
    "Shows": {
        "indexes": [],
        "schema": {
            "_id": {"type": "ObjectId"},
            "show_id": {"type": "str"},
            "title": {"type": "str"},
            "type": {"type": "str"},
            "description": {"type": "str"},
            "duration": {"type": "str"},
            "cast_ids": {"type": "list"},
            "genre_ids": {"type": "list"},
            "ratings_id": {"type": "ObjectId"}
        }
    }
}
