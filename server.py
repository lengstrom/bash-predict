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

class CommandHandler(tornado.web.RequestHandler):
    def get(self):
        pos = int(self.get_argument('position'))
        words = str(self.get_argument('words')).split()
        predicted = get_predicted(words, pos)
        self.write(predicted)

if __name__ == "__main__":
    corpus_path = 'final.txt'
    with open(corpus_path) as f:
        lines = f.readlines()

    counts = get_token_counts(lines)
    min_occurances = 0

    def verify(word):
        if type(word) == str:
            word = word.strip()
        if counts[word] >= min_occurances:
            return True
        return False

    model = NGramModel(lines, verify, n = 4)
    model31 = NGramModel31(lines, verify, n = 4)

    def process_input(inp, idx):
        inp = (convert_to_tokens(verify))(inp)
        if len(inp) == idx:
            #return self.predict_ngram(filter(self.verify, inp)[-self.N:])
            return model.predict_ngram(inp[-(model.N-1):idx])
        else:
            return model31.predict_ngram(inp[idx-((model.N-1)-1):idx] + inp[idx:idx+1])

    app = tornado.web.Application([
        (r"/", CommandHandler)
    ])
    
    server = tornado.httpserver.HTTPServer(app)
    server.listen(5000)
    tornado.ioloop.IOLoop.instance().start()
