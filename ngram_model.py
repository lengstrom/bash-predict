import cPickle, heapq
from collections import Counter
         
def get_token_counts(lines):
    all_tokens = Counter()

    for i in lines:
        tokens = map(lambda x: x.strip(), i.split())
        all_tokens.update(tokens)

    return all_tokens

class NGramModel:
    def __init__(self, corpus_sentences):
        possible_tokens = {}
        n = 0
        for i in corpus_sentences:
            for j in i:
                if j in possible_tokens:
                    n += 1


        for i in corpus_sentences:
            self.process_sentence(sentence)

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
