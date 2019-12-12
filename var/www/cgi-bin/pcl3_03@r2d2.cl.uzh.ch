#!/usr/bin/python3

import cgi
import cgitb
import io
import gzip
from gensim.models.fasttext import FastText
from sklearn import metrics
import numpy as np
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
    for item in data:
        if item == word:
            pass
        else:
            distances[item] = metrics.pairwise.cosine_distances([data[item]], [data[word]])
    key_min = min(distances.keys(), key=(lambda k: distances[k]))
    print('Min. Distanz')
    print(key_min)
    return(key_min)

#if __name__ == "__main__":
    #find_synonyms("../../../cc.de.300.vec", 'und')