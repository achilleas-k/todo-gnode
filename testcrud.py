"""
Very simple straightforward testing of CRUD operations on a single item.
"""
from bson.objectid import ObjectId
from dbmanager import DatabaseManager
from taskitem import TaskItem

db = DatabaseManager()
taskid = ObjectId()  # ID to use in test
testitem = TaskItem(_id=taskid, user_id="123abc", description="Test CRUD",
                   priority=1, done=False)

def create():
    db.create(testitem)
    print("Item created")
    read()

def read():
    theitem = db.read(taskid)[0]
    print(theitem.document())
    assert theitem.document() == testitem.document(), "Documents do not match"

def update():
    testitem.done = True
    print("Item updated")
    db.update(testitem)
    read()

def delete():
    db.delete(testitem)
    print("Item deleted")
    assert len(db.read(taskid)) == 0, "Item remains after deletion"

if __name__=="__main__":
    create()
    update()
    delete()
