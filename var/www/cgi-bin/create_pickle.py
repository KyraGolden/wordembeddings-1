import pickle
import io

fin = io.open('../../../50000.cc.de.300.vec', 'r', encoding='utf-8', newline='\n', errors='ignore')
n, d = map(int, fin.readline().split())
data = {}

for line in fin:
#line = fin.readline()
    tokens = str(line).split(' ')
    data[tokens[0]] = tokens[1:]
    #print(tokens[0])
    #print(data[tokens[0]])
#print(data)

output = open('50000_word_vecs.pkl', 'wb')
pickle.dump(data, output)
output.close()