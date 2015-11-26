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
                    (r"/list", ListHandler),
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
        self.render_list()

    def post(self):
        user_id = self.get_secure_cookie("user")
        description = self.get_argument("description", None)
        if description is None:
            return
        newitem = TaskItem(user_id=user_id, description=description)
        self.db.create(newitem)
        self.render_list()

    def render_list(self):
        user_id = self.get_secure_cookie("user")
        items = self.db.read({"user_id": user_id})
        self.render("list.html", items=items)

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
        elif action == "toggle":
            self.toggle(taskitem)

    def delete(self, taskitem):
        if taskitem:
            # print(taskitem.document())
            self.db.delete(taskitem)
        self.redirect("/list")

    def toggledone(self, taskitem):
        taskitem.done ^= True
        self.db.update(taskitem)
        self.redirect("/list")

class WelcomeHandler(BaseHandler):
    def get(self):
        if not self.current_user:
            self.write('<html><body>Welcome! Please <a href="/login">login</a>'
                       '</body></html>')
            return
        name = tornado.escape.xhtml_escape(self.current_user)
        self.write('<html><body>Welcome {name}!<br>'
                   'Go to <a href=/list>todo list</a>'
                   '</body></html>'.format(name=name))

class LoginHandler(BaseHandler):
    def get(self):
        self.write('<html><body><form action="/login" method="post">'
                   'Name: <input type="text" name="name">'
                   '<input type="submit" value="Sign in">'
                   '</form></body></html>')

    def post(self):
        self.set_secure_cookie("user", self.get_argument("name"))
        self.redirect("/")

def main():
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(8989)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
