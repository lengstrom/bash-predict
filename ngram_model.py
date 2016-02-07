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
        if self.best_succ == None || self.successor[token].count > self.best_count:
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
        index = 1
        # while look to try to use up to k tokens to base prediction
        while index <= k:
            if input[len(input) - index] in root.successor:
                index += 1
            else:
                break 
        #we now have index start position
        tokens = input[len(input) - index:len(input) - 1]
        if not input[len(input) - index] in root.successor:
            return ""
        else:
            last_node = root.successor[tokens[0]]
        for i in range(1:len(tokens)):
            last_node = last_node.successor[tokens[i]]

        return last_node.best_succ




if __name__ == "__main__":
    _, corpus_path = sys.argv
    with open(corpus_path) as f:
        lines = f.readlines()

    counts = get_token_counts(lines)
    K = 15 # number of counts before

    #DECLARE ROOT HERE 

    def is_wildcard(token):
        return counts[token.strip()] < K + 1
