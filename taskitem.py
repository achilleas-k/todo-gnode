"""
The task object class. Using this class (instead of plain dictionaries)
enforces document structure.
"""
from bson.objectid import ObjectId


class TaskItem(object):
    def __init__(self, _id=None, user_id=None, description=None,
                 date_due=None, priority=-1, done=False):
        if _id is None:
            self._id = ObjectId()
        else:
            self._id = _id
        self.user_id = user_id
        self.description = description
        self.date_due = date_due
        self.priority = priority
        self.done = done

    def document(self):
        """
        Return dictionary representation of this TaskItem.
        """
        return self.__dict__
