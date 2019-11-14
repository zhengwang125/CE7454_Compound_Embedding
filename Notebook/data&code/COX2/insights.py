import networkx as nx
import matplotlib.pyplot as plt
import pickle
import heapq
from matplotlib_venn import venn2

def stat(Tokens):
    freq = {}
    for token in Tokens:
        for i in token:
            if i in freq:
                freq[i] = freq[i] + 1
            else:
                freq[i] = 1
    return freq

def draw_bar(freq):
    temp = []
    for key, value in freq.items():
        temp.append((key, value))
    freq_sort = heapq.nlargest(len(freq), temp, key=lambda x:x[1])
    xticks = []
    for p in freq_sort:
        xticks.append(p[0])
    plt.bar(range(len(freq)), [freq.get(xtick, 0) for xtick in xticks], align='center', yerr=0.000001)
    plt.semilogy()
    plt.xlabel('Token')
    plt.ylabel('Frequency')
    plt.title('Compound Atomic Group')
    plt.show()
    return freq_sort

def draw_pattern(id):
    print(corpus_to_id[id])
    temp = {}
    for key in PATTERN[Lookup[id][0]][Lookup[id][1]]:
        temp[key] = G_labeldict[Lookup[id][0]][key]
    print(temp)
    nx.draw(G_collection[Lookup[id][0]].subgraph(PATTERN[Lookup[id][0]][Lookup[id][1]]), labels = temp, with_labels = True, node_color='y', node_size = 200, font_size=10)
    plt.show()

if __name__ == '__main__':
    Graph_Label_list = pickle.load(open('Graph_Label_list', 'rb'), encoding='bytes')
    G_collection = pickle.load(open('G_collection', 'rb'), encoding='bytes')
    G_labeldict = pickle.load(open('G_labeldict', 'rb'), encoding='bytes')
    PATTERN = pickle.load(open('PATTERN', 'rb'), encoding='bytes')
    corpus = pickle.load(open('corpus', 'rb'), encoding='bytes')
    Tokens = pickle.load(open('Tokens', 'rb'), encoding='bytes')
    Lookup = pickle.load(open('Lookup', 'rb'), encoding='bytes')
    corpus_to_id = {v: k for k, v in corpus.items()}
    freq = stat(Tokens)
    freq_sort = draw_bar(freq)
    print('The most frequent 10 patterns')
    for i in range(10):
        print('Token_id, Frequency:', freq_sort[i][0], freq_sort[i][1])
        draw_pattern(freq_sort[i][0])
    print('The least frequent 10 patterns')
    for i in range(1, 11):
        print('Token_id, Frequency:', freq_sort[-i][0], freq_sort[-i][1])
        draw_pattern(freq_sort[-i][0])
    positive = set()
    negative = set()
    for i in range(len(Tokens)):
        for t in Tokens[i]:
            if Graph_Label_list[i] == 1:
                positive.add(t)
            else:
                negative.add(t)
    v = venn2([positive, negative], ('Class_1', 'Class_-1'))
    plt.show()
    po = positive.difference(negative)
    no = negative.difference(positive)
    pn = positive&negative
    print('Class_1 only:', po, 'length =', len(po))
    print('Class_-1 only:', no, 'length =', len(no))
    print('Class_1 & Class_-1:', pn, 'length =', len(pn))
    print('visualize patterns only exist in Class_1 (pIC50>6.5)')
    for i in po:
        print('Token_id, Frequency:', freq_sort[i][0], freq_sort[i][1])
        draw_pattern(freq_sort[i][0])
    print('visualize patterns only exist in Class_-1 (pIC50<6.5)')
    for i in no:
        print('Token_id, Frequency:', freq_sort[i][0], freq_sort[i][1])
        draw_pattern(freq_sort[i][0])

#    #token reduction
#    Tokens = pickle.load(open('Tokens', 'rb'), encoding='bytes')
#    Graph_Label_list = pickle.load(open('Graph_Label_list', 'rb'), encoding='bytes')
#    positive = set()
#    negative = set()
#    for i in range(len(Tokens)):
#        for t in Tokens[i]:
#            if Graph_Label_list[i] == 1:
#                positive.add(t)
#            else:
#                negative.add(t)
#    
#    pn = positive&negative
#    Tokens_reduction = []
#    for i in range(len(Tokens)):
#        temp = []
#        for t in Tokens[i]:
#            if t in pn:
#                continue
#            else:
#                temp.append(t)
#        Tokens_reduction.append(temp)