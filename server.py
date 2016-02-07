import pdb, time, cv2, os, platform
import tornado.httpserver
import tornado.ioloop
import numpy as np
import tornado.web
from tornado.options import define, options

def get_predicted(words, pos):
    # get predicted word
    pass
    return "PREDICTED_WORD"

class CommandHandler(tornado.web.RequestHandler):
    def get(self):
        pos = int(self.get_argument('position'))
        words = str(self.get_argument('words')).split()
        predicted = get_predicted(words, pos)
        self.write(predicted)

if __name__ == "__main__":
    app = tornado.web.Application([
        (r"/", CommandHandler)
    ])
    
    server = tornado.httpserver.HTTPServer(app)
    server.listen(5000)
    tornado.ioloop.IOLoop.instance().start()
