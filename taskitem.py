"""
The task object class. Using this class (instead of plain dictionaries)
enforces document structure.
"""
from bson.objectid import ObjectId
from utils import parse_date

class TaskItem(object):
    def __init__(self, _id=None, user_id=None, taskname=None,
                 description=None, datetime_due=None, priority=-1, done=False):
        self._id = _id or ObjectId()
        self.user_id = user_id
        self.taskname = taskname
        self.description = description
        self.datetime_due = datetime_due
        self.priority = priority
        self.done = done

    def document(self):
        """
        Return dictionary representation of this TaskItem.
        """
        return self.__dict__

    def idstr(self):
        """
        Return a string representation of the TaskItem ID for use in templates.
        """
        return str(self._id)

    @property
    def due_today(self):
        """Returns true if the task is due today or if it is overdue"""
        return self.datetime_due and (self.datetime_due - parse_date("now")).days < 0
