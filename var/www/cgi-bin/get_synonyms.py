#!/usr/bin/python3

import cgi
import cgitb
import io
import json
import re
import pickle
import gzip
#from gensim.models.fasttext import FastText
from sklearn import metrics
import numpy as np
cgitb.enable(display=0, logdir="/logs")

def application(environ, start_response):
    params = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)
    word_orig = params["w"].value
    word_lower = word_orig.lower()
    sprache_wort = params["sprache_wort"].value
    nr = params["nr"].value
    sprache_wordemb = params["sprache_wordemb"].value
    searchType = params["st"].value
    synonym = find_synonyms(searchType, sprache_wordemb, sprache_wort, word_orig, word_lower, int(nr))
    output = {}
    output["syn1"] = synonym
    output_js = json.dumps(output)
    status = "200 OK"
    output_js = output_js.encode()
    response_headers = [("Content-type", "application/json; charset=UTF-8"),
                        ("Content-Length", str(len(output_js)))]
    start_response(status, response_headers)
    return [output_js]

def find_synonyms(searchType, sprache_wordemb, sprache_wort, word_orig, word_lower, anzahl):
    if searchType == 'bigSearch' and sprache_wort == 'd':
        if sprache_wort == sprache_wordemb:
            fname_w = "/home/pcl3_03/public_html/wordembeddings/10000.cc.de.300.vec"
        else:
            fname_w = "/home/pcl3_03/public_html/wordembeddings/10000.wiki.de.align.vec"
    elif searchType == 'bigSearch':
        if sprache_wort == sprache_wordemb:
            fname_w = "/home/pcl3_03/public_html/wordembeddings/10000.cc.en.300.vec"
        else:
            fname_w = "/home/pcl3_03/public_html/wordembeddings/10000.wiki.en.align.vec"
    elif searchType == 'quickSearch' and sprache_wort == 'd':
        if sprache_wort == sprache_wordemb:
            fname_w = "/home/pcl3_03/public_html/wordembeddings/5000.cc.de.300.vec"
        else:
            fname_w = "/home/pcl3_03/public_html/wordembeddings/5000.wiki.de.align.vec"
    else:
        if sprache_wort == sprache_wordemb:
            fname_w = "/home/pcl3_03/public_html/wordembeddings/5000.cc.en.300.vec"
        else:
            fname_w = "/home/pcl3_03/public_html/wordembeddings/5000.wiki.en.align.vec"
    if sprache_wort == sprache_wordemb:
        fin = io.open(fname_w, 'r', encoding='utf-8', newline='\n', errors='ignore')
        data = {}
        for line in fin:
            # line = fin.readline()
            tokens = str(line).split(' ')
            data[tokens[0]] = tokens[1:]
        distances = {}
        out_list = []
        for item in data:
            if item == word_orig:
                pass
            else:
                try:
                    distances[item] = metrics.pairwise.cosine_distances([data[item]], [data[word_orig]])
                except KeyError:
                    return "Dieses Wort befindet sich nicht in der Sammlung."
                except ValueError:
                    pass
        ctr = 0
        while ctr < anzahl:
            key_min = min(distances.keys(), key=(lambda k: distances[k]))
            out_list.append(key_min)
            del distances[key_min]
            ctr += 1
        seperator = ', '
        return seperator.join(out_list)
        #return(key_min)
    else:
        if searchType == 'bigSearch' and sprache_wordemb == 'd':
            #fname_we = "/home/pcl3_03/public_html/wordembeddings/50000.cc.de.300.vec"
            fname_we = "/home/pcl3_03/public_html/wordembeddings/10000.wiki.de.align.vec"
        elif searchType == 'bigSearch':
            #fname_we = "/home/pcl3_03/public_html/wordembeddings/50000.cc.en.300.vec"
            fname_we = "/home/pcl3_03/public_html/wordembeddings/10000.wiki.en.align.vec"
        elif searchType == 'quickSearch' and sprache_wordemb == 'd':
            #fname_we = "/home/pcl3_03/public_html/wordembeddings/10000.cc.de.300.vec"
            fname_we = "/home/pcl3_03/public_html/wordembeddings/5000.wiki.de.align.vec"
        else:
            #fname_we = "/home/pcl3_03/public_html/wordembeddings/10000.cc.en.300.vec"
            fname_we = "/home/pcl3_03/public_html/wordembeddings/5000.wiki.en.align.vec"
        fin_w = io.open(fname_w, 'r', encoding='utf-8', newline='\n', errors='ignore')
        data_w = {}
        word_found = False
        for line in fin_w:
            # line = fin.readline()
            tokens = str(line).split(' ')
            data_w[tokens[0]] = tokens[1:]
            if tokens[0] == word_lower:
                word_vec = data_w[tokens[0]]
                word_found = True
                break
        if word_found:
            fin_we = io.open(fname_we, 'r', encoding='utf-8', newline='\n', errors='ignore')
            data_we = {}
            for line in fin_we:
                # line = fin.readline()
                tokens = str(line).split(' ')
                data_we[tokens[0]] = tokens[1:]
            distances = {}
            out_list = []
            for item in data_we:
                try:
                    distances[item] = metrics.pairwise.cosine_distances([data_we[item]], [data_w[word_lower]])
                except ValueError:
                    pass
            ctr = 0
            while ctr < anzahl:
                key_min = min(distances.keys(), key=(lambda k: distances[k]))
                out_list.append(key_min)
                del distances[key_min]
                ctr += 1
            seperator = ', '
            return seperator.join(out_list)
            #return(key_min)
        else:
            return "Dieses Wort befindet sich nicht in der Sammlung."


if __name__ == "__main__":
    searchType = 'quickSearch'
    sprache_wordemb = 'd'
    sprache_wort = 'd'
    word_orig = 'bla'
    word_lower = 'bla'
    anzahl = 3
    print(find_synonyms(searchType, sprache_wordemb, sprache_wort, word_orig, word_lower, anzahl))
