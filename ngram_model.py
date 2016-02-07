import cPickle, pdb
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
    for i in range(len(line)):
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

    out.append(process_line(line[last_n:i]))
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
    def __init__(self, value):
        self.successors = {}
        self.value = value
        self.count = 1
        self.best_succ = None #the child that is most probable, and how many times it occurs
        self.best_count = 0

    def add_successor(self, token):
        if not token in self.successors:
            successor = NGramNode(token)
            self.successors[token] = token
        else:
            successor = self.successors[token]
            successor.count += 1

        #Update most likely successor 
        if token != '____' and self.best_succ == None or successor.count > self.best_count:
            self.best_succ = token
            self.best_count = successor.count

        return successor

    def add_successor_chain(self, tokens):
        prev = self
        for i in tokens:
            if not verify(i):
                i = "____"
            prev = prev.add_successor(i)

class NGramModel:
    def __init__(self, corpus_sentences, verify, n = 3):
        self.root = NGramNode("")
        self.verify = verify
        self.N = n
        i = 0
        for sentence in corpus_sentences:
            i += 1
            self.process_sentence(sentence)
            if i % 1000 == 0:
                print i

    def process_sentence(self, sentence):
        tokens = sentence.split()
        for idx, token in enumerate(tokens):
            tokens = sentence[idx:idx+self.N]#filter(self.verify, sentence[idx:])[:self.N]
            if tokens:
                self.root.add_successor_chain(tokens)

    def predict_ngram(self, inp):
        if len(inp) == 0:
            return ""

        prev = self.root
        for i in inp:
            prev = self.root[i]
        return prev.best_succ

    def process_input(self, inp, idx): # idx is the index of the element of inp where
        # the predicted output should be after
        inp = map(convert_to_tokens(self.verify), inp)
        if len(inp) == idx:
            #return self.predict_ngram(filter(self.verify, inp)[-self.N:])
            return self.predict_ngram(inp[-self.N:])
        else:
            return self.predict_31_ngram(inp[idx-(self.N-1):idx + 1])
           # to_pred = filter(self.verify, inp[:idx])[-(self.N-1):] + filter(self.verify, inp[idx:])[0:1]
           # return self.predict_2s_ngram(to_pred)

if __name__ == "__main__":
    corpus_path = 'toy.txt'
    with open(corpus_path) as f:
        lines = f.readlines()

    counts = get_token_counts(lines)
    min_occurances = 20

    def verify(word):
        if counts[word.strip()] >= min_occurances:
            return True
        return False
        
    model = NGramModel(lines, verify, n = 3)
    #pdb.set_trace()
    best_succ = model.process_input('a b c', 3)
    print best_succ
