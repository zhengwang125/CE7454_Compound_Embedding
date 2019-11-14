import pickle
import heapq
import matplotlib.pyplot as plt
from gensim.models.doc2vec import Doc2Vec, TaggedDocument

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

def build_graph_collection(Tokens):
    res = []
    id = 0
    for token in Tokens:
        t = []
        for n in token:
            t.append(str(n))
        res.append(TaggedDocument(t, ['g_'+ str(id)]))
        id = id + 1
    return res

if __name__ == '__main__':
    corpus = pickle.load(open('corpus', 'rb'), encoding='bytes')
    Tokens = pickle.load(open('Tokens', 'rb'), encoding='bytes')
    freq = stat(Tokens)
    draw_bar(freq)
    document_collections = build_graph_collection(Tokens)
    model = Doc2Vec(document_collections,
                    size = 10,
                    window = 2,
                    min_count = 1,
                    dm = 1,
                    workers = 1,
                    iter = 5000,
                    alpha = 0.01,
                    hs = 0,
                    negative = 2)
    model.save('models/graph-dm.model')