from flask import Flask, abort, request, Response
from flask_cors import CORS
import time
import json
import pymongo

import db

mongo_client = pymongo.MongoClient("mongodb://localhost:27017")
save_my_thesis_db = mongo_client["savemythesisdb"]
version_collection = save_my_thesis_db["versions"]

app = Flask(__name__)
CORS(app)

def data_to_response(response_data):
    json_response = json.dumps(response_data)
    response = Response(json_response,
                        content_type = "application/json; charset=utf-8")
    response.headers.add("content-length", len(json_response))
    return response

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/history")
def get_history():
    history = db.get_history(version_collection)
    response = data_to_response(history)
    response.status_code = 200
    return response

@app.route("/version/<version_id>")
def get_version_by_id(version_id):
    version = db.get_version_by_id(version_collection, int(version_id))
    if version is None:
        response = data_to_response({})
        return response
    response = data_to_response(version)
    response.status_code = 200
    return response

counter = 0

@app.route("/version", methods=["POST"])
def post_version():
    if not request.json:
        abort(400)
    request_json = request.get_json()
    versions = [
        {
            "_id": int(time.time()),
            "timestamp": int(time.time()),
            "text": request_json["text"],
            "author": request_json["author"],
            "commitTitle": "Correct spelling",
            "commitText": "Correct spellings of 5 words.",
        },
        {
            "_id": int(time.time()),
            "timestamp": int(time.time()),
            "text": request_json["text"],
            "author": request_json["author"],
            "commitTitle": "Add section",
            "commitText": "Section about 'computer program', 'breakthrough image possible', 'Katie Bouman'",
        },
        {
            "_id": int(time.time()),
            "timestamp": int(time.time()),
            "text": request_json["text"],
            "author": request_json["author"],
            "commitTitle": "Change section",
            "commitText": "Change content to be about 'wrong visual effects', 'Kip Thorne'",
        },
    ]
    global counter
    db.insert_version(version_collection, versions[counter])
    response = data_to_response(versions[counter])
    response.status_code = 200
    counter += 1
    return response

if __name__ == "__main__":
    app.run()