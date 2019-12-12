import io
import gzip
from gensim.models.fasttext import FastText
from sklearn import metrics
import numpy as np

def find_synonyms(fname, word):
    #lines = [x.decode('utf8').strip() for x in fname.readlines()]
    fin = io.open(fname, 'r', encoding='utf-8', newline='\n', errors='ignore')
    n, d = map(int, fin.readline().split())
    #print(fin.readline().split())
    data = {}
    #for line in fin:
    counter = 0
    while counter < 5000:
        line = fin.readline()
        #print(line)
        #tokens = line.rstrip().split(' ')
        tokens = str(line).split(' ')
        #print('Tokens: ')
        #print(tokens)
        #das untere geht viel länger als das obere
        #data[tokens[0]] = map(float, tokens[1:])
        data[tokens[0]] = tokens[1:]
        #print('Data: ')
        #print(data)
        counter += 1
        #print("Cosine similarity to " + word + ": ")
    distances = {}
    for item in data:
        #print(item)
        if item == word:
            pass
        else:
            distance = metrics.pairwise.cosine_distances([data[item]], [data[word]])
            #Bsp. König
            if distance > 0.3 and distance < 0.5:
                distances[item] = distance
        #print(metrics.pairwise.cosine_distances([data[item]], [data[word]]))
    key_min = min(distances.keys(), key=(lambda k: distances[k]))
    print('Min. Distanz')
    print(key_min)
    print(distances[key_min])
    return(key_min)


if __name__ == "__main__":
    find_synonyms("../../../cc.de.300.vec", 'Betreuung')