import cPickle, heapq, Queue
from collections import Counter

k = 3
         
def get_token_counts(lines):
    all_tokens = Counter()

    for i in lines:
        tokens = map(lambda x: x.strip(), i.split())
        all_tokens.update(tokens)

    return all_tokens

class NGramNode:

    def __init__(self, value):
        self.successor = {}
        self.value = value
        self.count = 1
        self.best_succ = None #the child that is most probable, and how many times it occurs
        self.best_count = 0

    def add_successor(self, token):
        if not token in self.successor:
            self.successor[token] = NGramNode(token)
        else:
            self.successor[token].count += 1

        #Update most likely successor 
        if self.best_succ == null || self.successor[token].count > self.best_count:
            self.best_succ = token
            self.best_count = self.successor[token].count

        return self.successor[token]

class NGramModel:
    def __init__(self, corpus_sentences, root):
        for i in corpus_sentences:
            self.process_sentence(sentence, root)

    def process_sentence(self, sentence, root):
        sentence = sentence.split()
        index = 0;
        for index in range(len(sentence))
            node = root.add_successor(sentence[index])
            tokens = sentence[i:i+k]
            last_node = node
            for token in tokens:
                n = last_node.add_successor(token)
                last_node = n

    def process_input(input, root):
        input = input.split()
        if len(input) > k:
            tokens = input[len(input) - k:len(input)]    
        else:
            tokens = input[i:i+len(input)]   
        n = root.successor[tokens[0]]
        for t in tokens:







if __name__ == "__main__":
    _, corpus_path = sys.argv
    with open(corpus_path) as f:
        lines = f.readlines()

    counts = get_token_counts(lines)
    K = 15 # number of counts before

    #DECLARE ROOT HERE 

    def is_wildcard(token):
        return counts[token.strip()] < K + 1
