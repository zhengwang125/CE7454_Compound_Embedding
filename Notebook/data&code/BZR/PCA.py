import pickle 
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_recall_fscore_support
from sklearn.model_selection import train_test_split

import numpy as np
from sklearn.decomposition import PCA


def take_second(elem):
    return elem[1]

def build_graph_collection(G_labeldict, Node_Attribute_list):
    Element_dict={'':0,'H':1,'He':2,'Li':3,'Be':4,'B':5,
              'C':6,'N':7,'O':8,'F':9,'Ne':10,'Na':11,
              'Mg':12,'Al':13,'Si':14,'P':15,'S':16,'Cl':17,
              'Ar':18,'K':19,'Ca':20,'Sc':21,'Ti':22,'V':23,
              'Cr':24,'Mn':25,'Fe':26,'Co':27,'Ni':28,'Cu':29,
              'Zn':30,'Ga':31,'Ge':32,'As':33,'Se':34,'Br':35,
              'Kr':36,'Rb':37,'Sr':38,'Y':39,'Zr':40,'Nb':41,
              'Mo':42,'Tc':43,'Ru':44,'Rh':45,'Pd':46,'Ag':47,
              'Cd':48,'In':49,'Sn':50,'Sb':51,'Te':52,'I':53,'Xe':54}
    res = []
    count = 0
    for G in G_labeldict:
        t = []
        for n in G:
            tmp = [Element_dict[G[n]], Node_Attribute_list[n][0]]
            t.append(tmp)
        t.sort(key = take_second)
        part = [0 for n in range(80)]
        for i in range(len(t)):
            part[i] = t[i][0]
        if len(part) > count:
            count = len(part)
        res.append(part)
    return np.array(res)

if __name__ == '__main__':
    G_labeldict = pickle.load(open('G_labeldict', 'rb'), encoding='bytes')
    Node_Attribute_list = pickle.load(open('Node_Attribute', 'rb'), encoding='bytes')
    Graph_Label_list = pickle.load(open('Graph_Label_list', 'rb'), encoding='bytes')
    graph_collection = build_graph_collection(G_labeldict, Node_Attribute_list)
    print(graph_collection)
    pca = PCA(n_components=10)
    X = pca.fit_transform(graph_collection)
    Y = np.array(Graph_Label_list) 

    print(X)
    x_train, x_test, y_train, y_test = train_test_split(X, Y, random_state=1, train_size=0.6)
    
    clf = SVC(C=6, kernel='rbf', gamma='auto', decision_function_shape='ovr')
    clf.fit(x_train, y_train.ravel())
    y_hat = clf.predict(x_train)
  
    print('training set accuracy:', accuracy_score(y_hat, y_train))
    y_hat = clf.predict(x_test)
    print('testing set accuracy:', accuracy_score(y_hat, y_test))
    # precision is the ratio tp / (tp + fp)
    # recall is the ratio tp / (tp + fn)
    #F1 harmonic mean of the precision and recall
    # col[0]=results of -1, col[1]=results of 1 
    print('precision, recall, fscore, support', precision_recall_fscore_support(y_test, y_hat, labels=[-1]))
