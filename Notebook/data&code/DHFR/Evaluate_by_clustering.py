from sklearn.cluster import KMeans
from sklearn import metrics
from gensim.models.doc2vec import Doc2Vec
import pickle
import numpy as np

def get_vector(path, label):
    model = Doc2Vec.load(path)
    RES = []
    for i in range(len(label)):
        RES.append(model.docvecs['g_'+str(i)])
    RES = np.array(RES)
    estimator = KMeans(n_clusters = 2)
    estimator.fit(RES)
    label_pred = estimator.labels_ 

    return metrics.normalized_mutual_info_score(label, label_pred), metrics.adjusted_rand_score(label, label_pred), label, label_pred

if __name__ == '__main__':
    path_dbow = './models/graph-dbow.model'  
    Graph_Label_list = pickle.load(open('Graph_Label_list', 'rb'), encoding='bytes')
    
    nmi, ari, label_true, label_pred = get_vector(path_dbow, Graph_Label_list)
    print('normalized mutual info score', nmi)
    print('adjusted rand score', ari)