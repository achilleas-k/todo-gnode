import os
import tornado.httpserver
import tornado.ioloop
import tornado.web
from dbmanager import DatabaseManager
from taskitem import TaskItem
from bson.objectid import ObjectId


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [(r"/", WelcomeHandler),
                    (r"/login", LoginHandler),
                    (r"/logout", LogoutHandler),
                    (r"/list", ListHandler),
                    (r"/new", NewItemHandler),
                    (r"/action/(\w+)/(\w+)", ActionHandler),
                   ]
        settings = dict(
                    title="TODO LIST",
                    cookie_secret="SOME_RANDOM_VALUE",
                    template_path=os.path.join(os.path.dirname(__file__),
                                                 "templates"),
                    static_path=os.path.join(os.path.dirname(__file__),
                                             "static"),
                    autoreload=True,
                    debug=True)
        super(Application, self).__init__(handlers, **settings)
        self.db = DatabaseManager()

class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

    def get_current_user(self):
        user_id = self.get_secure_cookie("user")
        if not user_id:
            return None
        return user_id

class ListHandler(BaseHandler):
    def get(self):
        user_id = self.get_secure_cookie("user")
        items = self.db.read({"user_id": user_id})
        self.render("list.html", username=user_id, items=items)

class ActionHandler(BaseHandler):
    def get(self, action, task_id):
        # make sure the task belongs to the current user
        user_id = self.get_secure_cookie("user")
        if not user_id:
            return  # TODO: raise error
        taskitem = self.db.read_id(ObjectId(task_id))
        if taskitem.user_id != user_id:
            return  # TODO: raise error

        if action == "delete":
            self.delete(taskitem)
        elif action == "toggledone":
            self.toggledone(taskitem)

    def delete(self, taskitem):
        if taskitem:
            # print(taskitem.document())
            self.db.delete(taskitem)
        self.redirect("/list")

    def toggledone(self, taskitem):
        taskitem.done ^= True
        self.db.update(taskitem)
        self.redirect("/list")

class NewItemHandler(BaseHandler):
    def post(self):
        user_id = self.get_secure_cookie("user")
        description = self.get_argument("description", None)
        if description.strip():
            newitem = TaskItem(user_id=user_id, description=description)
            self.db.create(newitem)
        self.redirect("/list")



class WelcomeHandler(BaseHandler):
    def get(self):
        if not self.current_user:
            self.redirect("/login")
        else:
            self.redirect("/list")

class LoginHandler(BaseHandler):
    def get(self):
        self.render("login.html")

    def post(self):
        self.set_secure_cookie("user", self.get_argument("name"))
        self.redirect("/")

class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.redirect(self.get_argument("next", "/"))

def main():
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(8989)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
