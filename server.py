import os
import tornado.web
import tornado.ioloop
from tornado.web import RequestHandler
from tornado.options import define, options
from tornado.websocket import WebSocketHandler

define("port", default=8888, help="run on the given port", type=int)

class HomeHandler(RequestHandler):
    def get(self):
        self.render("home.html")

class ChatHandler(WebSocketHandler):

    users = []
    
    # Client open WS
    def open(self):
        self.users.append(self)
        # Server send message to clients
        print("[%s]:上線囉" % (self.request.remote_ip))
        for user in self.users:
            user.write_message(u"[%s] 上線囉"%(self.request.remote_ip))
    
    # Client send message to server
    def on_message(self, msg):
        print("[%s]: %s" % (self.request.remote_ip, msg))
        for user in self.users:
            user.write_message(u"[%s] : %s"%(self.request.remote_ip, msg))
    
    # Client close WS
    def on_close(self):
        self.users.remove(self)
        # Server send message to clients
        print("[%s]:下線了" % (self.request.remote_ip))
        for user in self.users:
            user.write_message(u"u[%s] 下線了"%(self.request.remote_ip))
 
    
    # Server close WS
    def close(self):
        pass
    
    # check client source
    def check_origin(self, origin):
        return True

if __name__ == "__main__":
    app = tornado.web.Application(
        [
            (r"/", HomeHandler),
            (r"/chat", ChatHandler),
        ],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
    )
    app.listen(options.port)
    print("listening on %d" % (options.port))
    tornado.ioloop.IOLoop.current().start()