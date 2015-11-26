"""
Basic CRUD operations for MongoDB with collection name `todo`.
"""
from pymongo import MongoClient


class DatabaseManager(object):

    def __init__(self):
        self.client = MongoClient(host="localhost", port=27017)
        self.database = self.client["todo"]

    def create(self, item):
        if item is not None:
            self.database.todo.insert(item)
        else:
            pass  # TODO: raise exception

    def read(self, item_id=None):
        if item_id is None:
            return self.database.todo.find()
        else:
            return self.database.todo.find({"_id": item_id})

    def update(self, item):
        if item is not None:
            self.database.todo.save(item)
        else:
            pass  # TODO: raise exception

    def delete(self, item):
        if item is not None:
            self.database.todo.remove(item)
        else:
            pass  # TODO: raise exception
