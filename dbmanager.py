"""
Basic CRUD operations for MongoDB with collection name `todo`.

`item`s are of type TaskItem
"""
from pymongo import MongoClient
from taskitem import TaskItem


class DatabaseManager(object):

    def __init__(self):
        self.client = MongoClient(host="localhost", port=27017)
        self.database = self.client["todo"]

    def create(self, item):
        if item is not None:
            self.database.todo.insert(item.document())
        else:
            pass  # TODO: raise exception

    def read(self, item_id=None):
        if item_id is None:
            cursor = self.database.todo.find()
        else:
            cursor = self.database.todo.find({"_id": item_id})
        items = []
        for document in cursor:
            items.append(TaskItem(**document))
        return items

    def update(self, item):
        if item is not None:
            self.database.todo.save(item.document())
        else:
            pass  # TODO: raise exception

    def delete(self, item):
        if item is not None:
            self.database.todo.remove(item.document())
        else:
            pass  # TODO: raise exception
