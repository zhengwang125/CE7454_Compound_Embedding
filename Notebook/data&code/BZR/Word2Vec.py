import pickle
from gensim.models import Word2Vec 

def build_graph_collection(G_labeldict):
    res = []
    for G in G_labeldict:
        t = []
        for n in G:
            t.append(G[n])
        res.append(t)
    return res

if __name__ == '__main__':
    G_labeldict = pickle.load(open('G_labeldict', 'rb'), encoding='bytes')
    document_collections = build_graph_collection(G_labeldict)
    model = Word2Vec(document_collections,
                    size = 10,
                    window = 2,
                    min_count = 1,
                    workers = 1,
                    iter = 5000,
                    alpha = 0.01,
                    hs = 0,
                    sg = 0,
                    negative = 2)

    model.save('models/word2vec.model')