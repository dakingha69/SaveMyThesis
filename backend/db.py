import pymongo

def insert_version(collection, version):
    inserted_doc = collection.insert_one(version)
    return inserted_doc.inserted_id

def get_version_by_id(collection, version_id):
    doc = collection.find_one({ "_id": version_id })
    return doc

def get_history(collection):
    docs = []
    for doc in collection.find().sort("timestamp", pymongo.DESCENDING):
        doc["_id"] = str(doc["_id"])
        docs.append(doc)
    return docs

