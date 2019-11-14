import pickle
from gensim.models.doc2vec import Doc2Vec, TaggedDocument

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
    document_collections = build_graph_collection(Tokens)
    model = Doc2Vec(document_collections,
                    size = 10,
                    window = 2,
                    min_count = 1,
                    dm = 0,
                    workers = 1,
                    iter = 4000,
                    alpha = 0.01,
                    hs = 0,
                    negative = 2)
    model.save('models/graph-dbow.model')