#!/usr/bin/python3

import cgi
import cgitb
import io
import json
import gzip
from gensim.models.fasttext import FastText
from sklearn import metrics
import numpy as np
cgitb.enable(display=0, logdir="/logs")


def application(environ, start_response):
    params = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)
    word = params["s"].value
    nr =  params["nr"].value
    synonym = find_synonyms("/home/pcl3_03/public_html/wordembeddings/short.cc.de.300.vec", word, int(nr))
    output = {}
    output["syn1"] = str(synonym)
    output_js = json.dumps(output)
    output = "<h2> Here are " + nr + " synonyms for " + word + ":</h2><br><p>" + synonym + "</p>"
    status = "200 OK"
    output_js = output_js.encode()
    response_headers = [("Content-type", "application/json; charset=UTF-8"),
                        ("Content-Length", str(len(output_js)))]
    start_response(status, response_headers)
    return [output_js]

def find_synonyms(fname, word, anzahl):
    fin = io.open(fname, 'r', encoding='utf-8', newline='\n', errors='ignore')
    n, d = map(int, fin.readline().split())
    data = {}
    #for line in fin:
    counter = 0
    #counter-Limit kann rauf-/runtergesetzt werden (damit Abfragen nicht so lange dauern), im File gibt es aber nur
    #1000 Einträge.
    while counter < 999:
        line = fin.readline()
        tokens = str(line).split(' ')
        data[tokens[0]] = tokens[1:]
        counter += 1
    distances = {}
    out_list = []
    for item in data:
        if item == word:
            pass
        else:
            try:
                distances[item] = metrics.pairwise.cosine_distances([data[item]], [data[word]])
            except KeyError:
                #print("Dieses Wort befindet sich nicht in der Datenbank")
                return "Dieses Wort befindet sich nicht in der Datenbank"
    ctr = 0
    while ctr < anzahl:
        key_min = min(distances.keys(), key=(lambda k: distances[k]))
        out_list.append(key_min)
        del distances[key_min]
        #print('Min. Distanz')
        #print(key_min)
        ctr += 1
    seperator = ', '
    return seperator.join(out_list)
    #return(key_min)

if __name__ == "__main__":
    find_synonyms("../../../cc.de.300.vec", 'Hilferuf')