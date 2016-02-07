import pdb, time, cv2, os, platform
import tornado.httpserver
import tornado.ioloop
import numpy as np
import tornado.web
from tornado.options import define, options

class CommandHandler(tornado.web.RequestHandler):
    def get(self):
        pdb.set_trace()

if __name__ == "__main__":
    app = tornado.web.Application([
        (r"/", CommandHandler)
    ])
    
    server = tornado.httpserver.HTTPServer(app)
    server.listen(5000)
    tornado.ioloop.IOLoop.instance().start()
