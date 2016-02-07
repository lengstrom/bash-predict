import pdb, os
import cPickle as pickle
from collections import Counter

# helpers
def get_token_counts(lines):
    all_tokens = Counter()
    for i in lines:
        tokens = map(lambda x: x.strip(), i.split())
        all_tokens.update(tokens)

    return all_tokens

def tokenize(v):
    if v[-1] == '/':
        return '_DIRECTORY_'

    try:
        idx = v.index('://')
        return '_' + v[:idx+3].upper() + '_'
    except:
        pass

    _, ext = os.path.splitext(v)
    ext = ext.lower()
    if ext:
        return ("_" + ext + "_").upper()

    return v

def process_line(line):
    line_frags = line.split()
    n = 0
    for i, v in enumerate(line_frags):
        if '=' in v:
            n += 1
        else:
            break

    line_frags = line_frags[n:]
    # for i, v in enumerate(line_frags):
    #     replace_token(v, line_frags, i)

    line2 = " ".join(line_frags)
    return line2

def parse_line(line, verify):
    curr_quote = False
    quotes = set(['\'', '"'])
    out = []
    last_n = 0
    for i in xrange(0, len(line)):
        char = line[i]
        if char in quotes:
            if curr_quote == False:
                curr_quote = char
            elif curr_quote == char:
                if not (line[i-1] == '\\' and not (i < 2 and line[i-2] == '\\')):
                    curr_quote = False
        if curr_quote != False:
            if line[i] == ' ':
                line = line[:i] + '_' + line[i+1:]

    out.append(process_line(line[last_n:i+1]))
    concat = "".join(out)
    string = concat.replace('\'', '').replace('"', '').replace('\ ', '_')

    line = string.split()
    repl_w = {i.strip() : tokenize(i.strip()).strip() for i in line if not verify(i.strip())}
    for idx, token in enumerate(line):
        if token.strip() in repl_w:
            if idx > 0 and line[idx - 1].strip() != '|':
                line[idx] = repl_w[token]

    return line

def convert_to_tokens(verify):
    def true_tokenize(string):
        line = parse_line(string, verify)
        return line
    return true_tokenize

class NGramNode:
    def __init__(self, value, n = 4):
        self.successors = {}
        self.value = value
        self.count = 1
        self.N = n
        self.best_succ = None #the child that is most probable, and how many times it occurs
        self.best_count = 0

    def add_successor(self, token):
        if not token in self.successors:
            successor = NGramNode(token)
            self.successors[token] = successor
        else:
            successor = self.successors[token]
            successor.count += 1

        #Update most likely successor 
        if token != '____' and self.best_succ == None or successor.count > self.best_count:
            self.best_succ = token
            self.best_count = successor.count

        return successor

    def add_successor_chain(self, tokens, verify):
        prev = self
        length = len(tokens)
        if length < self.N:
            tokens = range(self.N - length)[::-1] + tokens
        for i in tokens:
            if type(i) == str and not verify(i):
                i = "____"
            prev = prev.add_successor(i)

class NGramModel:
    def __init__(self, corpus_sentences, verify, n = 4):
        self.root = NGramNode("")
        self.verify = verify
        self.N = n
        i = 0
        for sentence in corpus_sentences:
            i += 1
            self.process_sentence(sentence)
            if i % 100000 == 0:
                print i

    def process_sentence(self, sentence):
        all_tokens = sentence.split()
        for idx, token in enumerate(all_tokens):
            tokens = all_tokens[idx:idx+self.N]#filter(self.verify, sentence[idx:])[:self.N]
            if tokens:
                self.root.add_successor_chain(tokens, self.verify)

    def predict_ngram(self, inp):
        length = len(inp)
        if length == 0:
            return ""

        N = self.N - 1
        if length < N:
            inp = range(N - length)[::-1] + inp

        prev = self.root
        for i in inp:
            if not i in prev.successors:
                i = '____'
                if not i in prev.successors:
                    i = prev.best_succ
                    if not i in prev.successors:
                        return False
            prev = prev.successors[i]

        top_succ = filter(lambda x: not (x[0][0] == '_' and x[0][-1] == '_'), sorted([(i, prev.successors[i].count) for i in prev.successors], key = lambda x: x[0]))[-5:]
        return top_succ

class NGramModel31(NGramModel):
    # def __init__(self, corpus_sentences, verify, n = 3):
    #     super()
    def process_sentence(self, sentence):
        all_tokens = sentence.split()
        stop = len(all_tokens) - 1
        for idx, token in enumerate(all_tokens):
            if idx == 0:
                continue
            #assert len(tokens) == self.N
            tokens = all_tokens[max(0, idx-(self.N-1)):idx - 1] + all_tokens[idx:idx+1] + all_tokens[idx-1:idx] #filter(self.verify, sentence[idx:])[:self.N]
            if tokens:
                self.root.add_successor_chain(tokens, self.verify)

    def predict_ngram(self, inp):
        length = len(inp)
        if length == 0:
            return ""

        N = self.N - 1
        if length < N:
            inp = range(N - length)[::-1] + inp

        prev = self.root
        for i in inp:
            if not i in prev.successors:
                i = '____'
                if not i in prev.successors:
                    i = prev.best_succ
                    if not i in prev.successors:
                        return False
            prev = prev.successors[i]
        top_succ = filter(lambda x: not (x[0][0] == '_' and x[0][-1] == '_'), sorted([(i, prev.successors[i].count) for i in prev.successors], key = lambda x: x[0]))[-5:]
        return top_succ
#        return prev.best_succ


class Verify(object):
    def __init__(self, counts, min_occurances):
        self.counts = counts
        self.min_occurances = min_occurances

    def __call__(self, word):
        if type(word) == str:
            word = word.strip()
        if self.counts[word] >= self.min_occurances:
            return True
        return False

def extract_model(corpus_path):
    with open(corpus_path) as f:
        lines = f.readlines()

    counts = get_token_counts(lines)
    min_occurances = 40

    verify = Verify(counts, min_occurances)

    try:
        with open('model.pickle', 'rb') as f:
            model = pickle.load(f)
    except:
        print 'Building model'
        model = NGramModel(lines, verify, n = 4)
        with open('model.pickle', 'wb') as f:
            pickle.dump(model, f)
    else:
        print 'Loaded pickled model'
    try:
        with open('model31.pickle', 'rb') as f:
            model31 = pickle.load(f)
    except:
        print 'Building model31'
        model31 = NGramModel31(lines, verify, n = 4)
        with open('model31.pickle', 'wb') as f:
            pickle.dump(model31, f)
    else:
        print 'Loaded pickled model31'

    models = (model, model31)
    # pickle models
    def process_input(inp, idx):
        inp = (convert_to_tokens(verify))(inp)
        N = model.N - 1
        if len(inp) == idx:
            #return self.predict_ngram(filter(self.verify, inp)[-self.N:])
            to_pred = inp[max(0, -(model.N-1)):idx]
            if len(to_pred) > 0:
                return model.predict_ngram(to_pred)
            print "empty query!"
            return []
        else:
            #to_pred = inp[idx:idx+1] + inp[max(0,idx-((model.N-1)-1)):idx]
            to_pred = inp[max(0, idx-(N-1)):idx+1]
            if len(to_pred) > 0:
                return model31.predict_ngram(to_pred)
            print "empty query!"
            return []

    def get_predicted(words, pos):
        # get predicted word
        whitespaces = 0
        curr = False
        started=False
        wordlen = len(words)
        for i, v in enumerate(words):
            if v.isspace() and started == True:
                if curr == False:
                    whitespaces += 1
                    curr = True
                else:
                    curr = False
            else:
                if not v.isspace():
                    started=True
                if i == wordlen - 1:
                    whitespaces += 1
            if pos == i:
                break

        res = process_input(words, whitespaces)
        res = filter(lambda x: not (x[0] == '_' and x[-1] == "_"), res)
        if res == False:
            return ""
        return " ".join([i[0] for i in res])

    return model31, model, process_input, get_predicted

if __name__ == "__main__":
    corpus_path = 'final.txt'
    model31, model, process_input, get_predicted = extract_model(corpus_path)
    best_succ = process_input('tar _.XZ_', 1)
    print best_succ
