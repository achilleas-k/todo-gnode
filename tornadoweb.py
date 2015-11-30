#!/usr/bin/env python
from __future__ import print_function

import os
import sys
import tornado.httpserver
import tornado.ioloop
import tornado.web
from dbmanager import DatabaseManager
from taskitem import TaskItem
from bson.objectid import ObjectId
from utils import parse_date


class Application(tornado.web.Application):
    def __init__(self):

        handlers = [(u"/", WelcomeHandler),
                    (u"/login", LoginHandler),
                    (u"/logout", LogoutHandler),
                    (u"/list", ListHandler),
                    (u"/new", NewItemHandler),
                    (r"/action/(\w+)/(\w+)", ActionHandler),
                   ]
        settings = {"title": "TODO LIST",
                    "login_url": "/login",
                    "cookie_secret": open("cookie_secret").read().replace("\n", ""),
                    "template_path": os.path.join(os.path.dirname(__file__),
                                                 "templates"),
                    "static_path": os.path.join(os.path.dirname(__file__),
                                             "static"),
                    "autoreload": True,
                    "debug": True}

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
    @tornado.web.authenticated
    def get(self):
        user_id = self.get_secure_cookie("user")
        items = self.db.read({"user_id": user_id})
        self.render("list.html", username=user_id, items=items)


class ActionHandler(BaseHandler):
    @tornado.web.authenticated
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
    @tornado.web.authenticated
    def get(self):
        pass

    def post(self):
        user_id = self.get_secure_cookie("user")
        taskname = self.get_argument("taskname", "")
        description = self.get_argument("description", "")
        date = parse_date(self.get_argument("datetime", ""))
        if taskname.strip():
            newitem = TaskItem(user_id=user_id,
                               taskname=taskname,
                               datetime_due=date,
                               description=description)
            self.db.create(newitem)
        self.redirect("/list")


class WelcomeHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
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
    port = 8989
    print("Listening on port %d" % port, file=sys.stderr)
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
