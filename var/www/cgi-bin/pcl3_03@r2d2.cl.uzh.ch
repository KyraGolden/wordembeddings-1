#!/usr/bin/python3

import cgi
import cgitb
import io
import gzip
from gensim.models.fasttext import FastText
from sklearn import metrics
from sklearn.manifold import TSNE
from matplotlib import pyplot as plt
import numpy as np
import pylab
cgitb.enable(display=0, logdir="/logs")


def application(environ, start_response):
    params = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)
    word = params["word"].value
    nr =  params["nr"].value
    synonym = find_synonyms("/home/pcl3_03/public_html/wordembeddings/short.cc.de.300.vec", word)
    output = "<h2> Here are " + nr + " synonyms for " + word + ":</h2><br><p>" + synonym + "</p>"
    status = "200 OK"
    output = output.encode()
    response_headers = [("Content-type", "text/html; charset=UTF-8"),
                        ("Content-Length", str(len(output)))]
    start_response(status, response_headers)
    return [output]

def find_synonyms(fname, word):
    fin = io.open(fname, 'r', encoding='utf-8', newline='\n', errors='ignore')
    n, d = map(int, fin.readline().split())
    data = {}
    #for line in fin:
    counter = 0
    #counter-Limit kann rauf-/runtergesetzt werden (damit Abfragen nicht so lange dauern)
    while counter < 300:
        line = fin.readline()
        tokens = str(line).split(' ')
        data[tokens[0]] = tokens[1:]
        counter += 1
        distances = {}
    X = np.empty((0, 300))
    for item in data:
        # print(item)
        if item.lower() == word.lower():
            pass
        else:
            # Bsp. Königx
         try:
            distance = metrics.pairwise.cosine_distances([data[item]], [data[word]])
            if 0.3 < distance < 0.5:
                distances[item] = distance
                # save the n vectors
                vec = np.array(data[item], dtype=float)
                X = np.append(X, [vec], axis=0)
         except ValueError:
             pass


    #add original vector to array
    help2 = np.array(data[word], dtype=float)
    X = np.append(X,[help2],axis = 0)

    tsne = TSNE(n_components=2, random_state=0)
    np.set_printoptions(suppress=True)
    Y = tsne.fit_transform(X)
    x_coords = Y[:, 0]
    y_coords = Y[:, 1]
    # display scatter plot
    plt.scatter(x_coords, y_coords)
    X = np.append(X, [help2], axis=0)
    listofkeys = list(distances.keys())
    listofkeys.append(word)
    #for label, x, y in zip(listofkeys.format(y), x_coords, y_coords):
    for i, txt in enumerate(listofkeys):
        plt.annotate(txt, (x_coords[i], y_coords[i]))
    plt.xlim(x_coords.min() + 0.00005, x_coords.max() + 0.00005)
    plt.ylim(y_coords.min() + 0.00005, y_coords.max() + 0.00005)
    plt.savefig('wordembeddings-1/images/vectors.png')
    key_min = min(distances.keys(), key=(lambda k: distances[k]))
    print('Min. Distanz')
    print(key_min)
    return(key_min)

#if __name__ == "__main__":
    #find_synonyms("../../../cc.de.300.vec", 'und')
