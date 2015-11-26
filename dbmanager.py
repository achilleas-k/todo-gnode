"""
Basic CRUD operations for MongoDB with collection name todo.
items are of type TaskItem
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

    def read(self, fields):
        """Return items that match arbitrary field values"""
        cursor = self.database.todo.find(fields)
        return [TaskItem(**document) for document in cursor]

    def read_all(self):
        """Return all items in the database"""
        cursor = self.database.todo.find()
        return [TaskItem(**document) for document in cursor]

    def read_id(self, item_id):
        """Return single item that matches the given item_id or None if the
        item does not exist
        """
        results = self.read({"_id": item_id})
        if len(results) == 1:
            return results[0]
        elif len(results) > 1:
            # this shouldn't happen
            raise Exception("_id duplicates found in database")
        else:
            return None

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
