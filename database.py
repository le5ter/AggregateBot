from pymongo import MongoClient


def get_collection():
    connection_string = "mongodb://localhost:27017/"
    client = MongoClient(connection_string)

    db = client["AggregateBot"]
    return db["AggregateBot"]
