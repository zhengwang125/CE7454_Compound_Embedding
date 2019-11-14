from sklearn.model_selection import train_test_split
from gensim.models import Word2Vec
import pickle
import numpy as np
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_recall_fscore_support

def get_vector(g_labeldict, path, label):
    model = Word2Vec.load(path)
    RES = []
    dim = 10
    for i in range(len(label)):
        graphvec = np.zeros(dim)
        for token in g_labeldict[i]:
            graphvec += np.array(model.wv[g_labeldict[i][token]])
        graphvec / len(g_labeldict[i])
        RES.append(graphvec.tolist())
    return np.array(RES), np.array(label)

if __name__ == '__main__':
    path_dbow = './models/word2vec.model'  
    Graph_Label_list = pickle.load(open('Graph_Label_list', 'rb'), encoding='bytes')
    G_labeldict = pickle.load(open('G_labeldict', 'rb'), encoding='bytes')
    X, Y = get_vector(G_labeldict, path_dbow, Graph_Label_list)
    
    x_train, x_test, y_train, y_test = train_test_split(X, Y, random_state=1, train_size=0.6)
    
    clf = SVC(C=2, kernel='rbf', gamma='auto', decision_function_shape='ovr')
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