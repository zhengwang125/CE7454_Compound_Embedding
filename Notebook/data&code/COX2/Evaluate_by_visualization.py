from sklearn.manifold import TSNE
from gensim.models.doc2vec import Doc2Vec
import pickle
import numpy as np
import matplotlib.pyplot as plt
from sklearn import manifold

def get_vector(path, label):
    model = Doc2Vec.load(path)
    RES = []
    for i in range(len(label)):
        RES.append(model.docvecs['g_'+str(i)])
    return np.array(RES)
    
if __name__ == '__main__':
    path_dbow = './models/graph-dbow.model'  
    Graph_Label_list = pickle.load(open('Graph_Label_list', 'rb'), encoding='bytes')
    embeds = get_vector(path_dbow, Graph_Label_list)
    tsne = manifold.TSNE(n_components = 2, init = 'pca', random_state = 0)
    Y = tsne.fit_transform(embeds)
    plt.figure(figsize=(8, 8))
    plt.scatter(Y[:, 0], Y[:, 1], c=np.array(Graph_Label_list).reshape(-1))
    plt.legend()
