import pdb, time, cv2, os, platform
import tornado.httpserver
import tornado.ioloop
import numpy as np
import ngram_model
import tornado.web
from tornado.options import define, options

def get_predicted(words, pos):
    # get predicted word
    whitespaces = 0
    curr = False
    started = False
    for i, v in enumerate(words):
        if v.isspace() and started:
            if curr == False:
                whitespaces += 1
                curr = True
            else:
                curr = False
        else:
            started = True
            if i == len(words) - 1:
                whitespaces += 1
        if i == pos:
            break

    res = process_input(words, whitespaces)
    if res == False:
        return ""

    return " ".join(res)
archive = {
    
}
class CommandHandler(tornado.web.RequestHandler):
    def get(self):
        global archive
        pos = int(self.get_argument('position'))
        words = str(self.get_argument('words'))
        hashable = str(pos) + " " + words
        if hashable in archive:
            predicted = archive[hashable]
        else:
            predicted = get_predicted(words, pos)
            archive[hashable] = predicted
        self.write(predicted)
        #pdb.set_trace()

if __name__ == "__main__":
    print "Loading data..."
    model31, model, process_input, get_predicted = ngram_model.extract_model('final.txt')
    app = tornado.web.Application([
        (r"/", CommandHandler)
    ])
    print "    done"
    
    server = tornado.httpserver.HTTPServer(app)
    server.listen(5000)
    print "Started server!"
    tornado.ioloop.IOLoop.instance().start()
