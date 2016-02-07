import cPickle, heapq, Queue
from collections import Counter
         
def get_token_counts(lines):
    all_tokens = Counter()

    for i in lines:
        tokens = map(lambda x: x.strip(), i.split())
        all_tokens.update(tokens)

    return all_tokens

class NGramNode:
    def __init__(self):
        self.edges = {}

    def add_edge(self, edge):
        if not edge in self.edges:
            self.edges[edge] = NGramNode()

    def add_num(self, edge):
        pass

class NGramModel:
    def __init__(self, corpus_sentences):
        for i in corpus_sentences:
            self.process_sentence(sentence)

        self.model = 

    def process_sentence(self, sentence):
        pass

if __name__ == "__main__":
    _, corpus_path = sys.argv
    with open(corpus_path) as f:
        lines = f.readlines()

    counts = get_token_counts(lines)
    K = 15 # number of counts before

    def is_wildcard(token):
        return counts[token.strip()] < K + 1
