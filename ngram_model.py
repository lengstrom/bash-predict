import cPickle, heapq, Queue, pdb
from collections import Counter

#pdb.set_trace()

k = 3

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
        if self.best_succ == None or self.successor[token].count > self.best_count:
            self.best_succ = token
            self.best_count = self.successor[token].count

        return self.successor[token]

class NGramModel:
    def __init__(self, corpus_sentences, root):
        i = 0;
        for sentence in corpus_sentences:
            i += 1
            self.process_sentence(sentence, root)
            if i % 1000 == 0:
                print i

    def process_sentence(self, sentence, root):
        sentence = sentence.split()
        for index in xrange(0,len(sentence)):
            node = root.add_successor(sentence[index])
            tokens = sentence[index:index+k]
            last_node = node
            for token in tokens:
                n = last_node.add_successor(token)
                last_node = n

    def printTree(self, root):
        print "root " 
        print root.successor


    def process_input(self, input, root):
        print "processing input...."
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
        for i in xrange(1,len(tokens)):
            last_node = last_node.successor[tokens[i]]

        print last_node.best_succ
        return last_node.best_succ


if __name__ == "__main__":
    corpus_path = '/Users/sarahwooders/projects/bash-predict/text.txt'
    with open(corpus_path) as f:
        lines = f.readlines()

    root = NGramNode("")
    model = NGramModel(lines, root)
    #pdb.set_trace()
    i = raw_input('Enter input: ')
    model.printTree(root)
    model.process_input(i, root)

